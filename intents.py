import json
import sys
import ast
import os
import httplib, urllib, base64

import config

config_data = config.getConfig()

###########################################################
### get the current list of intents for the application ###
###########################################################
def getCurrentIntents(appID):
    """
        Takes appID as a parameter
        Returns the current Intents on the Application on the server
    """
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET","/luis/v1.0/prog/apps/{0}/intents?%{1}" .format(config_data["appID"], params),body_json, headers)

        print "Getting list of existing intents..."
        response = conn.getresponse()
        code = response.status
        if code == 200:
            current_intents = {}
            data = response.read()
            intents = ast.literal_eval(data)
            for intent in intents:
                current_intents[intent['name']] = intent['id']
            return current_intents
        else:
            return None
        conn.close()
    except Exception as e:
        print e

###############################
### get list of new intents ###
###############################
def getNewIntents():
    """
        Takes No Parameters
        Returns the list of intents in the config
    """
    new_intents = []
    basePath = "./intents/"
    for subdirs, dirs, files in os.walk(basePath):
        for file in files:
            filepath = subdirs + os.sep + file
            if filepath.endswith(".txt"):
                intent = filepath.split('/')[-1].split('.')[0]
                new_intents.append(intent)
    return new_intents

#######################################
### delete the intent with given id ###
#######################################
def deleteIntent(intentID):
    """
        Takes intentID as parameter
        Deletes the intent classifier with the intentID passed as parameter
    """
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    print "Deleting Intent..."

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("DELETE","/luis/v1.0/prog/apps/{0}/intents/{1}?{2}" .format(config_data["appID"], intentID, params),body_json, headers)
        response = conn.getresponse()
        code = response.status
        if code == 200:
            return True
        else:
            return False
    except Exception as e:
        print e