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
import imp
import csv
import copy
import time
import numpy as np
from easybayesy import NaiveBayesNetworkNode, NaiveBayesNetwork
from WhiteMatterNetwork import WhiteMatterNetwork

hasClosed = False
try:
    imp.find_module('BasalGangliaNetwork')
    hasClosed = True
    from BasalGangliaNetwork import BasalGangliaNetwork
except ImportError:
    hasClosed = False
# [END imports]




# [START create_app]
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'aries-key'

app.highlight = False
app.highlightText = "Highlight most discriminating features"

app.highlightTurnOn = 'Highlight most discriminating features'
app.highlightTurnOff =  '      Remove feature highlighting       '
app.setDxTitle = 'cleardx'
app.hasClosed = hasClosed

app.networks = [ 'White Matter' ]
if hasClosed:
    app.networks.append('Basal Ganglia')



Bootstrap(app)
# [END create_app]


def getPreviousFeatures( network, form ):
    previousFeatures = {}
    for k in form.keys():
        parts = k.split(":")
        if ( len(parts)==2 ) and (parts[0] == "last"):
            if network.has_node(parts[1]):
                previousFeatures[parts[1]] = form[k]
    return previousFeatures

def getNetwork( networkName ):
    if networkName == 'Basal Ganglia':
        return BasalGangliaNetwork()
    elif networkName == 'White Matter':
        return WhiteMatterNetwork()
    return None

@app.route('/about')
def about():
    return render_template('about.html', page='about')

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():

    print('%%%% index %%%%')
    print request.method

    highlightText = flask.current_app.highlightTurnOn
    highlightOn = "0"

    lastDx = flask.current_app.setDxTitle
    setDx = ''

    # For setting all features by diagnosis
    features = request.form.to_dict()


    networkName = flask.current_app.networks[0]
    lastNetwork = networkName

    ignoreFeatures = False

    if request.method == "GET":
        print( "*** GET action ***")
        print(features)

    previousFeatures = {}

    if features.has_key('lastHighlight'):
        highlightOn = features['lastHighlight']

    if features.has_key('lastNetwork'):
        lastNetwork = features['lastNetwork']

    network = getNetwork( lastNetwork )

    dxList = network.get_node_states("Diagnosis")

    if request.method == "POST":

        #print(features)


        print( "*** POST action ***")
        print( '--- Features ---')
        for k in features.keys():
            print( k + '=' + features[k])
        print( '--- End Features ---')

        if 'Network' in features:
            if features['Network'] != features['lastNetwork']:
                print("*** ACTION -> CHANGE NETWORK")
                lastNetwork = features['Network']
                ignoreFeatures = True
                network = getNetwork(lastNetwork)
                dxList = network.get_node_states("Diagnosis")

        if 'ClearDiagnosis' in features:
            print("*** ACTION -> CLEAR")
            setDx = 'cleardx'
            ignoreFeatures = True

        if features.has_key('HighlightFeatures'):
            print("HighlightFeatures is present")
            highlightAction = features['HighlightFeatures']
            if highlightAction == flask.current_app.highlightTurnOn:
                if highlightOn == "0":
                    print("*** ACTION -> HIGHLIGHT ON")
                    highlightOn = "1"
                    highlightText = flask.current_app.highlightTurnOff
            elif highlightAction == flask.current_app.highlightTurnOff:
                if highlightOn == "1":
                    print("*** ACTION -> HIGHLIGHT OFF")
                    highlightOn = "0"
                    highlightText = flask.current_app.highlightTurnOn
                    for n in network.nodeMap.keys():
                        network.nodes[ network.nodeMap[n] ].sensitive = ''
        else:
            if highlightOn == "0":
                highlightText = flask.current_app.highlightTurnOn
            elif highlightOn == "1":
                highlightText = flask.current_app.highlightTurnOff

        # Check if the 'SetDiagnosis' menu has changed
        if setDx == '':
            setDx = features.get('SetDiagnosis')
        lastDx = features.get('lastDx')
        if setDx != lastDx:
            print( '*** ACTION -> SET_DIAGNOSIS' )
            ignoreFeatures = True
            lastDx = setDx
            if ( setDx=='cleardx'):
                for n in network.nodes:
                    network.clear_node_state(n.name)
            else:
                dxIndex = dxList.index( setDx )
                network.set_node_states_by_result( dxIndex )

        # Set all network FeatureSelect
        previousFeatures = getPreviousFeatures(network, features)


        if not(ignoreFeatures):
            for k in features.keys():
                parts = features.get(k).split(":")
                if network.has_node(k):
                    state = ''
                    if ( len(parts) > 1 ):
                        network.set_node_state(k, parts[1] )
                        state = parts[1]
                    else:
                        network.clear_node_state(k)

                    if state != previousFeatures[k]:
                        setDx = 'cleardx'
                        lastDx = 'cleardx'
                        print(k + " changed from " + previousFeatures[k] + ' to ' + state)



    print("solve network: " + lastNetwork)
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

    if highlightOn == "1":
        print('Calculating sensitivities')
        for cat in network.categories:
            #print(cat)
            nodes = network.names_of_nodes_in_category(cat)
            maxSens = 0
            maxName = ''
            for n in nodes:
                network.nodes[ network.nodeMap[n] ].sensitive = ''
                if network.nodes[ network.nodeMap[n] ].value == '':
                    s = network.calculate_node_sensitivity(n, mat)
                    #print( n + ' ' + str(s))
                    if s > maxSens:
                        maxSens = s
                        maxName = n
            if maxName != '':
                network.nodes[ network.nodeMap[maxName] ].sensitive = 'sensitive'

    print('highlightOn = ' + highlightOn)

    return render_template('index.html',
        network=network,
        dx=dx,
        dxRad=dxRad,
        dxLength=len(dx),
        page='index',
        setDx=setDx,
        lastDx=lastDx,
        highlight=highlightText,
        highlightOn=highlightOn,
        networks=flask.current_app.networks,
        networkName=lastNetwork )

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
