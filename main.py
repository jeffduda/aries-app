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
import time
import numpy as np
from easybayesy import NaiveBayesNetworkNode, NaiveBayesNetwork
# [END imports]




# [START create_app]
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'aries-key'

app.highlight = False
app.highlightText = "Highlight most discriminating features"

app.network = NaiveBayesNetwork();
app.network.read_csv("/Users/jtduda/pkg/aries-app/BasalGangliaV2.csv")
app.dx = []
app.dxRad = []

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
    print('****')
    print('****')
    print(request.form)

    #network = NaiveBayesNetwork();
    #network.read_sheet("/Users/jtduda/pkg/aries-app/12-06-2018_BG_Bayesian_network_NaiveBayes.xlsx", "BGnetwork")
    #network.read_csv("/Users/jtduda/pkg/aries-app/BasalGangliaV2.csv")

    #network = flask.current_app.network

    dxList = flask.current_app.network.get_node_states("Diagnosis")
    setDx = ''

    # For setting all features by diagnosis
    features = request.form.to_dict()

    #if ( request.method=='POST'):
    forceResolve = False
    netTime = flask.current_app.network.modified

    if request.method == "POST":

        print( "--POST action")
        print( features
        )
        if 'ClearDiagnosis' in features:
            print("Clearing features")
            setDx = ''
            flask.current_app.network.reset()

        elif 'HighlightFeatures' in features:
            if flask.current_app.highlight == True:
                flask.current_app.highlight = False;
                flask.current_app.highlightText =  "Highlight most discriminating features"
                for n in flask.current_app.network.nodeMap.keys():
                    flask.current_app.network.nodes[ flask.current_app.network.nodeMap[n] ].sensitive = ''
            else:
                flask.current_app.highlight = True;
                flask.current_app.highlightText = "     Remove feature highlighting      "
                forceResolve = True

        elif 'SetDiagnosis' in features:
            setDx = features.get("SetDiagnosis")
            print( "Set features by diagnosis "+setDx)
            if ( setDx=="cleardx"):
                for n in flask.current_app.network.nodes:
                    flask.current_app.network.clear_node_state(n.name)
                setDx = ''
            else:
                dxIndex = dxList.index( setDx )
                flask.current_app.network.set_node_states_by_result( dxIndex )

        elif 'FeatureSelect' in features:
            print('Feature selection')
            for k in features.keys():
                parts = features.get(k).split(":")
                if flask.current_app.network.has_node(k):
                    if ( len(parts) > 1 ):
                        flask.current_app.network.set_node_state(k, parts[1] )
                    else:
                        flask.current_app.network.clear_node_state(k)

    print(netTime)
    print(flask.current_app.network.modified)

    if (flask.current_app.network.modified  > netTime) or forceResolve:
        print("network updated")
        sorted, mat =  flask.current_app.network.get_diagnoses(False)
        radSorted, radMat = flask.current_app.network.get_diagnoses(True)

        flask.current_app.dx = []
        flask.current_app.dxRad = []

        maxDx = 10
        if len(sorted) < maxDx:
            maxDx = len(sorted)

        cumSum = 0
        for i in range(maxDx):
            cumSum += mat[sorted[i]]
            flask.current_app.dx.append( (dxList[sorted[i]],mat[sorted[i]],cumSum) )

        cumSum = 0
        for i in range(len(radSorted)):
            cumSum += radMat[radSorted[i]]
            flask.current_app.dxRad.append( (dxList[radSorted[i]],radMat[radSorted[i]],cumSum) )

    if flask.current_app.highlight:
        print('Calculating sensitivities')
        for cat in flask.current_app.network.categories:
            print(cat)
            nodes = flask.current_app.network.names_of_nodes_in_category(cat)
            maxSens = 0
            maxName = ''
            for n in nodes:
                flask.current_app.network.nodes[ flask.current_app.network.nodeMap[n] ].sensitive = ''
                if flask.current_app.network.nodes[ flask.current_app.network.nodeMap[n] ].value == '':
                    s = flask.current_app.network.calculate_node_sensitivity(n, mat)
                    print( n + ' ' + str(s))
                    if s > maxSens:
                        maxSens = s
                        maxName = n
            if maxName != '':
                flask.current_app.network.nodes[ flask.current_app.network.nodeMap[maxName] ].sensitive = 'sensitive'


    return render_template('index.html',
        network=flask.current_app.network,
        dx=flask.current_app.dx,
        dxRad=flask.current_app.dxRad,
        dxLength=len(flask.current_app.dx),
        page='index',
        setDx=setDx,
        highlight=flask.current_app.highlightText)



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
