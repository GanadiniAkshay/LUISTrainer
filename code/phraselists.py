import httplib
import json

import config

configData = config.getConfig()
headers = {"Ocp-Apim-Subscription-Key": configData["subscription_key"], "Content-Type": "application/json"}


##################################################
### Get list of Phraselists of the Application ###
##################################################
def getExistingPhraselists():
    """
        Takes appID as a parameter
        Returns the current Phraselists on the Application on the server
    """
    try:
        print "Getting list of existing phraselists"
        currentPhraselists = None
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET", "/luis/v1.0/prog/apps/{0}/phraselists".format(configData["appID"]), None,
                     headers)
        response = conn.getresponse()
        if response.status == 200:
            phraselists = json.loads(response.read())
            currentPhraselists = {item.get("Name"): {"id": item.get("Id"), "phrases": item.get("Phrases")} for item in
                                  phraselists}
        conn.close()
        return currentPhraselists
    except Exception as e:
        print e


###################################
### Get list of new phraselists ###
###################################
def getNewPhraselists():
    """
        Takes No Parameters
        Returns the list of phraselists in the config
    """
    print "Getting list of new phraselists"
    return {item.get("name"): {"mode": item.get("mode"), "phrases": item.get("phrases")} for item in
            configData["phraselists"]}


###########################################
### Delete the phraselist with given id ###
###########################################
def deletePhraselist(id):
    """
        Takes id as parameter
        Deletes the phraselist with the id passed as parameter
    """
    print "Deleting Phraselist"
    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("DELETE",
                     "/luis/v1.0/prog/apps/{0}/phraselists/{1}?{2}".format(configData["appID"], id),
                     None, headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except Exception as e:
        print e


###############################
### Create a new Phraselist ###
###############################
def createPhraselist(name, phrases, mode):
    """
        Takes the phraselist name and phraselist phrases as parameters
        Creates a new phraselist with the given Entity Name
    """
    print "Creating Phraselist for " + name + ""
    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("POST", "/luis/v1.0/prog/apps/{0}/phraselists".format(configData["appID"]),
                     json.dumps({"Name": name, "Mode": mode, "Phrases": ",".join(phrases)}), headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 201
    except Exception as e:
        print e


###########################################
### Update the phraselist with given id ###
###########################################
def updatePhraselist(id, phrases, mode, name):
    """
        Takes id as parameter
        Updates the phraselist with the id passed as parameter
    """
    print "Updating " + name + ""
    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("PUT",
                     "/luis/v1.0/prog/apps/{0}/phraselists/{1}".format(configData["appID"], id),
                     json.dumps({"Name": name, "Mode": mode, "Phrases": ",".join(phrases), "IsActive": True}), headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except Exception as e:
        print e
