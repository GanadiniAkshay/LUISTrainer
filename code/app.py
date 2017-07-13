import httplib
import json

import config

configData = config.getConfig()
headers = {"Ocp-Apim-Subscription-Key": configData["subscription_key"]}


##################################
####  Create new application #####
##################################
def createApp():
    """
        Takes No Parameters
        Creates a new Application and adds the appID into config.json
    """
    print "Creating Application"
    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("POST", "/luis/v1.0/prog/apps", json.dumps({
            "Name": configData["name"],
            "Description": configData["description"],
            "Culture": configData["culture"]
        }), headers)
        data = conn.getresponse().read()
        configData["appID"] = data.replace("\"", "")
        config.updateConfig(configData)
        conn.close()
        print "Application Created"
    except Exception as e:
        print e


###########################################
### Get the application with a given id ###
###########################################
def getApplication():
    """
        Takes No Parameters
        Returns the True if the application exists
    """
    print "Checking if application exists"
    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET", "/luis/v1.0/prog/apps/{0}".format(configData["appID"]), None, headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except Exception as e:
        print e
