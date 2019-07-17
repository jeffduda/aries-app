# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
import flask
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import openpyxl
from openpyxl import Workbook, load_workbook
#import numpy as np
import os
import csv
import numpy as np
# [END imports]

class BayesNetForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

#class NetworkNode():
#    def __init__(self, name):
#        self.name = name

#    self.states=[]

#    def NumberOfStates():
#        return len(self.states)

class NaiveBayesNetworkNode:

    # Initializer
    def __init__(self, name, states):
        #self.name = name.replace('_', ' ')
        self.name = name
        self.states = states
        self.parent = ''
        self.category = ''
        self.menuStates = []
        self.menuStates.append(self.name)
        for s in self.states:
            self.menuStates.append(self.name+":"+s)
        self.value = ''
        self.menuValue = ''
        self.priors = np.ones(len(self.states))
        self.priors = self.priors / len(self.priors)
        self.probs = []
        self.hasChoice = ''
        self.sensitive = ''
        self.style = ''


    def set_parent(self, node):
        self.parent = node.name

    def is_state_selected(self, menuChoice):
        if menuChoice == self.menuValue:
            return 'selected'
        return ''



class NaiveBayesNetwork:

    def __init__(self):
        self.filename = ""
        self.name = "ExampleNetwork"
        self.categories = ["Signal", "Spatial", "Time", "Miscellaneous", "Clinical"];
        self.nodes = []
        self.nodeMap = {}

    def add_node(self, node):
        self.nodes.append(node)
        self.nodeMap[node.name] = len(self.nodes)-1
        print( node.name + str( len(self.nodes)-1 ))

    def has_node(self,name):
        return self.nodeMap.has_key(name)

    def get_node(self, name):
        if self.has_node(name):
            return self.nodes[ self.nodeMap[name] ]
        return None

    def get_node_states(self, name):
        if self.has_node(name):
            return self.nodes[ self.nodeMap[name] ].states
        return None

    def set_node_state(self, name, state):
        if self.has_node(name):
            n = self.nodeMap[name]
            if state in self.nodes[n].states:
                self.nodes[n].value = state
                self.nodes[n].menuValue = self.nodes[n].name + ':' + state
                self.nodes[n].hasChoice = 'hasChoice'
                self.nodes[n].sensitive = ''
            else:
                raise Exception("Invalid state set: " + state )

    def set_node_states_by_result(self, index):
        for n in self.nodes:
            if n.name != 'Diagnosis':
                vals = n.probs[index,:].tolist()
                state = vals.index(max(vals))
                self.set_node_state(n.name, n.states[state])

    def clear_node_state(self, name):
        if self.has_node(name):
            n = self.nodeMap[name]
            self.nodes[n].value = ''
            self.nodes[n].menuValue = ''
            self.nodes[n].hasChoice = ''
        else:
            raise Exception("Node does not exist: " + name )

    def set_node_probs(self, name, probs):
        if self.has_node(name):
            n = self.nodeMap[name]
            self.nodes[n].probs = probs
        else:
            raise Exception("Node does not exist: " + name )

    def get_node_priors(self, name):
        if self.has_node(name):
            return( self.nodes[ self.nodeMap[name] ].priors)
        return None

    def get_node_category(self, name):
        if self.has_node(name):
            return( self.nodes[ self.nodeMap[name] ].category)
        return None

    def number_of_nodes_in_category(self,category):
        count = 0
        for n in self.nodes:
            if n.category == category:
                count = count + 1
        return count

    def names_of_nodes_in_category(self,category):
        names = []
        for n in self.nodes:
            if n.category == category:
                names.append(n.name)
        return names

    def nodes_in_category(self,category):
        nodes = []
        for n in self.nodes:
            if n.category == category:
                nodes.append(n)
        return nodes

    def read_csv(self, network_file):
        self.filename = network_file

        diseases = []
        diseasePrior = []
        nodeNames = []
        nodeCategories = []
        nodeStates = []

        self.categories = []
        prob = []

        with open(self.filename) as csv_file:
            csv_reader =  csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if  line_count == 0:
                    allNodeStates = row[2:len(row)]

                    for n in allNodeStates:
                        nodeParts = n.split(":")
                        nodeCategories.append(nodeParts[0])
                        nodeNames.append(nodeParts[1])
                        nodeStates.append(nodeParts[2])

                    for n in np.unique(nodeNames):
                        states = []
                        cat = ''
                        for i in range(0,len(nodeNames)):
                            if nodeNames[i] == n:
                                states.append(nodeStates[i])
                                cat = nodeCategories[i]
                        node = NaiveBayesNetworkNode(n,states)
                        node.category = cat
                        node.parent = "Diagnosis"
                        self.add_node(node)

                else:
                    diseases.append(row[0])
                    diseasePrior.append(row[1])
                    rValues = row[2:]
                    prob.append(rValues)


                line_count += 1

        prob = np.vstack(prob)

        for n in self.nodes:
            nMat = np.empty((len(diseases), len(n.states) ))
            for s in range(0, len(n.states)):
                for i in range(0,len(nodeNames)):
                    if nodeNames[i] == n.name and n.states[s] == nodeStates[i]:
                        nMat[:,s] = prob[:,i]

            self.set_node_probs( n.name, nMat )

        dNode = NaiveBayesNetworkNode("Diagnosis", diseases)
        dNode.category = "Diagnosis"
        dNode.priors = diseasePrior
        self.add_node(dNode)
        self.categories = np.unique(nodeCategories)

    def calculate_node_sensitivity(self, name, currentProbs):

        if ( not(self.has_node(name)) ):
            return 0

        node = self.nodes[ self.nodeMap[name] ]
        val = node.value
        probs = currentProbs*0

        for v in range(len(node.states)):
            self.set_node_state(node.name, node.states[v])
            s, vProbs = self.get_diagnoses(False)
            probs += vProbs / ( currentProbs * node.probs[:,v] )
            probs[np.isnan(probs)] = 0

        if val == '':
            self.clear_node_state(node.name)
        else:
            self.set_node_state(node.name, val)

        sens = probs.sum()
        return sens


    def get_diagnoses(self, isRadiologic):
        mat = []
        if not(isRadiologic):
            mat.append(self.get_node_priors("Diagnosis"))
        else:
            unityPrior = []
            dis = self.get_node_priors("Diagnosis")
            for x in dis:
                unityPrior.append(1.0/len(dis))
            mat.append(unityPrior)

        for n in self.nodes:
            if (n.value != ''):
                if not(isRadiologic):
                    idx = n.states.index(n.value)
                    #print(n.name + ' ' + str(idx) + ' ' + n.value)
                    #print(n.probs)
                    #print( n.probs[:,idx])
                    mat.append( n.probs[:,idx])
                elif (n.category != "Clinical"):
                    #print(n.category + n.name)
                    idx = n.states.index(n.value)
                    mat.append( n.probs[:,idx])


        mat = np.vstack(mat)
        mat = mat.astype('double')
        mat = np.prod(mat, axis=0)
        mat = mat/np.sum(mat)
        sorted = np.argsort(mat)
        sorted = sorted[::-1]
        return sorted, mat


    def read_sheet(self, table_file, tableName):
    #    tableDir = "/home/jiancong/Desktop/projects/BayesNet/NaiveBayes/BasalGanglia/BG_Bayesian_network_NaiveBayes.xlsx"
    #    tableName = "BGnetwork"
        self.filename = table_file
        self.name = tableName

        wb=openpyxl.load_workbook(table_file)
        worksheet = wb[tableName]

        #Read the keys
        rows = list(worksheet.rows)
        first_row = rows[0]
        second_row = rows[1]

        keys = [c.value for c in first_row]
        values = [c.value for c in second_row]

        values = [v for v in values if v is not None]
        keys = keys[:len(values)]

        values = values[1:]
        keys = keys[1:]

        key_value_dict = {}

        current_k = ""
        for k, v, i in zip(keys, values, range(2, len(values) + 2)):
            if k is not None:
                current_k = k.split(" ")[0].upper()
                key_value_dict[current_k] = {v.split(" ")[0].upper():i - 2}
            else:
                key_value_dict[current_k][v.split(" ")[0].upper()] = i - 2

        # Read the probabilty
        disease = []
        prob = []
        for row in rows[2:]:
            row_values = [c.value for c in row if c.value is not None]

            if len(row_values) ==0:
                break

            if row_values[0] is None:
                break
            disease.append(row_values[0])
            prob.append(row_values[1:])
        prob = np.array(prob)
        prob = prob/100.0

        return disease, prob, key_value_dict



# [START create_app]
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'aries-key'

app.highlight = False
app.highlightText = "Highlight most discriminating features"

app.network = NaiveBayesNetwork();
app.network.read_csv("/Users/jtduda/pkg/aries-app/BasalGangliaV2.csv")

Bootstrap(app)
# [END create_app]


@app.route('/about')
def about():
    return render_template('about.html', page='about')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    #print('index')
    #print(request)
    print(request.form)

    #network = NaiveBayesNetwork();
    #network.read_sheet("/Users/jtduda/pkg/aries-app/12-06-2018_BG_Bayesian_network_NaiveBayes.xlsx", "BGnetwork")
    #network.read_csv("/Users/jtduda/pkg/aries-app/BasalGangliaV2.csv")

    network = flask.current_app.network

    dxList = network.get_node_states("Diagnosis")
    setDx = ''

    # For setting all features by diagnosis
    features = request.form.to_dict()

    #if ( request.method=='POST'):

    if 'ClearDiagnosis' in features:
        print("Clearing features")
        setDx = ''
        for n in network.nodes:
            network.clear_node_state(n.name)

    elif 'HighlightFeatures' in features:
        print("Highlight features swap state = " + str(flask.current_app.highlight))
        if flask.current_app.highlight == True:
            flask.current_app.highlight = False;
            flask.current_app.highlightText =  "Highlight most discriminating features"
            for n in network.nodeMap.keys():
                network.nodes[ network.nodeMap[n] ].sensitive = ''
        else:
            flask.current_app.highlight = True;
            flask.current_app.highlightText = "     Remove feature highlighting      "

        print("Now set to " + str(flask.current_app.highlight))

    elif 'SetDiagnosis' in features:
        setDx = features.get("SetDiagnosis")
        print( "Set features by diagnosis "+setDx)
        if ( setDx=="cleardx"):
            for n in network.nodes:
                network.clear_node_state(n.name)
            setDx = ''
        else:
            dxIndex = dxList.index( setDx )
            network.set_node_states_by_result( dxIndex )

    print('Feature selection')
    for k in features.keys():
        parts = features.get(k).split(":")
        if network.has_node(k):
            if ( len(parts) > 1 ):
                network.set_node_state(k, parts[1] )
            else:
                network.clear_node_state(k)

    sorted, mat =  network.get_diagnoses(False)
    radSorted, radMat = network.get_diagnoses(True)

    dx = []
    dxRad = []

    maxDx = 10
    if len(sorted) < maxDx:
        maxDx = len(sorted)

    cumSum = 0
    for i in range(maxDx):
        cumSum += mat[sorted[i]]
        dx.append( (dxList[sorted[i]],mat[sorted[i]],cumSum) )

    cumSum = 0
    for i in range(len(radSorted)):
        cumSum += radMat[radSorted[i]]
        dxRad.append( (dxList[radSorted[i]],radMat[radSorted[i]],cumSum) )

    if flask.current_app.highlight:
        print('Calculating sensitivities')
        for cat in network.categories:
            print(cat)
            nodes = network.names_of_nodes_in_category(cat)
            maxSens = 0
            maxName = ''
            for n in nodes:
                network.nodes[ network.nodeMap[n] ].sensitive = ''
                if network.nodes[ network.nodeMap[n] ].value == '':
                    s = network.calculate_node_sensitivity(n, mat)
                    print( n + ' ' + str(s))
                    if s > maxSens:
                        maxSens = s
                        maxName = n
            network.nodes[ network.nodeMap[maxName] ].sensitive = 'sensitive'


    return render_template('index.html', network=network, dx=dx, dxRad=dxRad, dxLength=len(dx), page='index', setDx=setDx, highlight=flask.current_app.highlightText)



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
