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
        self.name = name
        self.states = states
        self.parent = ''
        self.category = ''
        self.menuStates = []
        self.menuStates.append(name)
        for s in self.states:
            self.menuStates.append(name+":"+s)
        self.value = ''
        self.menuValue = ''
        self.priors = np.ones(len(self.states))
        self.priors = self.priors / len(self.priors)
        self.probs = []

    def set_parent(self, node):
        self.parent = node.name



class NaiveBayesNetwork:

    #def __init__(self, filename):
    #    self.filename = filename
       # read file and setup network

    def __init__(self):
        self.filename = ""
        self.name = "ExampleNetwork"
        self.categories = ["Signal", "Spatial", "Time", "Miscellaneous", "Clinical"];
        self.nodes = []

    def add_node(self, node):
        # error checking?
        self.nodes.append(node)

    def has_node(self,name):
        flag = False
        for n in self.nodes:
            if (flag==False):
                if n.name == name:
                    flag = True
        return flag

    def node_states(self, name):
        flag = False
        states = []
        for n in self.nodes:
            if (flag==False):
                if n.name == name:
                    flag = True
                    states = n.states
        return states

    def set_node_state(self, name, state):
        for n in self.nodes:
            if n.name == name:
                if state in n.states:
                    n.value = state
                    n.menuValue = n.name+':'+n.value
                else:
                    raise Exception("Invalid state set")

    def clear_node_state(self, name):
        for n in self.nodes:
            if n.name == name:
                n.value = ''
                n.menuValue = ''

    def set_node_probs(self, name, probs):
        for n in self.nodes:
            if n.name == name:
                n.probs = probs

    def get_node_priors(self, name):
        for n in self.nodes:
            if n.name == name:
                return(n.priors)

    def get_node_states(self, name):
        for n in self.nodes:
            if n.name == name:
                return(n.states)

    def get_node_category(self, name):
        for n in self.nodes:
            if n.name == name:
                return(n.category)

    def number_of_nodes_in_category(self,category):
        count = 0
        for n in self.nodes:
            if n.category == category:
                count = count + 1
        return count

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
                        self.nodes.append(node)

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
        self.nodes.append(dNode)
        self.categories = np.unique(nodeCategories)

        for n in self.nodes:
            st =  " ".join(str(x) for x in n.states)
            print( n.category + ' - ' + n.name + ' - ' + str(n.states))
            print(n.probs)

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
                    mat.append( n.probs[:,idx])
                elif (n.category != "Clinical"):
                    print(n.category + n.name)
                    idx = n.states.index(n.value)
                    mat.append( n.probs[:,idx])

        mat = np.vstack(mat)
        mat = mat.astype('float')
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
Bootstrap(app)
# [END create_app]



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    print('index')

    network = NaiveBayesNetwork();
    #network.read_sheet("/Users/jtduda/pkg/aries-app/12-06-2018_BG_Bayesian_network_NaiveBayes.xlsx", "BGnetwork")
    network.read_csv("/Users/jtduda/pkg/aries-app/BasalGangliaV2.csv")
    features = request.form.to_dict()
    for k in features.keys():

        parts = features.get(k).split(":")
        if ( len(parts) > 1 ):
            print(k + parts[1])
            network.set_node_state(k, parts[1] )
        else:
            network.clear_node_state(k)

    sorted, mat =  network.get_diagnoses(False)
    radSorted, radMat = network.get_diagnoses(True)

    dis = network.get_node_states("Diagnosis")
    dx = []
    dxRad = []

    maxDx = 10
    if len(sorted) < maxDx:
        maxDx = len(sorted)

    for i in range(maxDx):
        dx.append( (dis[sorted[i]],mat[sorted[i]]) )

    for i in range(len(radSorted)):
        dxRad.append( (dis[radSorted[i]],radMat[radSorted[i]]) )

    return render_template('index.html', network=network, dx=dx, dxRad=dxRad, dxLength=len(dx))



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
