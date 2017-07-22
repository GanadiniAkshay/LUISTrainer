import httplib
import json
import os

import config

configData = config.getConfig()
headers = {"Ocp-Apim-Subscription-Key": configData["subscription_key"], "Content-Type": "application/json"}


###########################################################
### Get the current list of intents for the application ###
###########################################################
def getExistingIntents():
    """
        Takes No Parameters
        Returns the current Intents on the Application on the server
    """
    print "Getting list of existing intents"
    try:
        currentIntents = None
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET", "/luis/v1.0/prog/apps/{0}/intents".format(configData["appID"]), None, headers)
        response = conn.getresponse()
        if response.status == 200:
            intents = json.loads(response.read())
            currentIntents = {item.get("name"): item.get("id") for item in intents.get("Result")}
        conn.close()
        return currentIntents
    except Exception as e:
        print e


###############################
### Get list of new intents ###
###############################
def getNewIntents():
    """
        Takes No Parameters
        Returns the list of intents in the config
    """
    print "Getting list of new intents"
    basePath = "../intents/"
    return [os.path.splitext(f)[0] for f in os.listdir(basePath) if
            os.path.isfile(os.path.join(basePath, f)) and f.endswith(".txt")]


#######################################
### Delete the intent with given id ###
#######################################
def deleteIntent(id):
    """
        Takes id as parameter
        Deletes the intent classifier with the id passed as parameter
    """
    print "Deleting Intent"
    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("DELETE", "/luis/v1.0/prog/apps/{0}/intents/{1}".format(configData["appID"], id), None,
                     headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except Exception as e:
        print e


######################################
### Create a new intent classifier ###
######################################
def createIntent(intent):
    """
        Takes intent as parameter
        Creates a new Intent Classifier with the given Intent Name
    """
    print "Creating Intent Classifier for " + intent + ""
    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("POST", "/luis/v1.0/prog/apps/{0}/intents".format(configData["appID"]),
                     json.dumps({"Name": intent}), headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 201
    except Exception as e:
        print e
