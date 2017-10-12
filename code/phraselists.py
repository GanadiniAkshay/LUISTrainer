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
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("GET", "/luis/api/v2.0/apps/{0}/versions/{1}/phraselists".format(configData["appID"], configData["activeVersion"]), None,
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
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("DELETE",
                     "/luis/api/v2.0/apps/{0}/versions/{1}/phraselists/{2}".format(configData["appID"], configData["activeVersion"], id),
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
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("POST", "/luis/api/v2.0/apps/{0}/versions/{1}/phraselists".format(configData["appID"], configData["activeVersion"]),
                     json.dumps({"Name": name, "IsExchangeable": mode, "Phrases": ",".join(phrases)}), headers)
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
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("PUT",
                     "/luis/api/v2.0/apps/{0}/versions/{1}/phraselists/{2}".format(configData["appID"], configData["activeVersion"], id),
                     json.dumps({"Name": name, "IsExchangeable": mode, "Phrases": ",".join(phrases), "IsActive": True}), headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except Exception as e:
        print e
