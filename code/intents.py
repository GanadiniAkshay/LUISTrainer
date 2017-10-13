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
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("GET", "/luis/api/v2.0/apps/{0}/versions/{1}/intents".format(configData["appID"], configData["activeVersion"]), None, headers)
        response = conn.getresponse()
        if response.status == 200:
            intents = json.loads(response.read())
            currentIntents = {item.get("name"): item.get("id") for item in intents}
        conn.close()
        return currentIntents
    except Exception as e:
        print e
        raise


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
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("DELETE", "/luis/api/v2.0/apps/{0}/versions/{1}/intents/{2}".format(configData["appID"], configData["activeVersion"], id), None,
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
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("POST", "/luis/api/v2.0/apps/{0}/versions/{1}/intents".format(configData["appID"], configData["activeVersion"]),
                     json.dumps({"Name": intent}), headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 201
    except Exception as e:
        print e
