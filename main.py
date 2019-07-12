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

class NaiveBayesNetwork():

    #def __init__(self, filename):
    #    self.filename = filename
       # read file and setup network

    def __init__(self):
        self.filename = ""
        self.name = "ExampleNetwork"
        self.categories = ["Signal", "Spatial", "Time", "Miscellaneous", "Clinical"];

    def read_csv(self, network_file):
        self.filename = network_file

        diseases = []
        nodeNames = []
        self.categories = []

        with open(self.filename) as csv_file:
            csv_reader =  csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if  line_count == 0:
                    nodeStates = row[2:len(row)-1]
                    print(nodeStates)
                    for n in nodeStates:
                        nodeParts = n.split(":")
                        nodeName = nodeParts[0] + ":" + nodeParts[1]
                        nodeNames.append(nodeName)
                        self.categories.append(nodeParts[0])
                   nodeNames = np.unique(nodeNames)

                   self.categories = np.unique(self.categories)

                else:
                    diseases.append(row[0])
                line_count += 1

        print( np.unique(nodeNames))

        print(self.categories)
        return diseases


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
    # make keys a dictionary
    keys = {"Disease":"Clear",
      "Colour":"Clear"
      }

    colours = ['Colour', 'Colour:Red', 'Colour:Blue', 'Colour:Black', 'Colour:Orange']

    form = BayesNetForm()
    cv = request.form.get('colour')

    keys['Colour'] = cv

    network = NaiveBayesNetwork();
    #network.read_sheet("/Users/jtduda/pkg/aries-app/12-06-2018_BG_Bayesian_network_NaiveBayes.xlsx", "BGnetwork")
    diseases = network.read_csv("/Users/jtduda/pkg/aries-app/example.csv")
    print(diseases)

    return render_template('index.html', colours=colours,keys=keys,form=form, network=network, diseases=diseases)

@app.route('/test', methods=['GET', 'POST'])
def test():
    cv = request.form.get('colour')
    return(str(cv))

# [START form]
@app.route('/form', methods=['GET'])
def form():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('form.html', colours=colours)
    #return render_template('form.html')
# [END form]



# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
