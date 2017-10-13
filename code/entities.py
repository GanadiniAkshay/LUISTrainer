import httplib
import json

import config

configData = config.getConfig()
headers = {"Ocp-Apim-Subscription-Key": configData["subscription_key"]}
headersWrite = {"Ocp-Apim-Subscription-Key": configData["subscription_key"], "Content-Type": "application/json"}


###############################################
### Get list of Entities of the Application ###
###############################################
def getExistingEntities():
    """
        Takes No Parameters
        Returns the current Entities on the Application on the server
    """
    print "Getting list of existing entities"
    try:
        currentEntities = None
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("GET", "/luis/api/v2.0/apps/{0}/versions/{1}/entities".format(configData["appID"], configData["activeVersion"]), None, headers)
        response = conn.getresponse()
        if response.status == 200:
            entities = json.loads(response.read())
            currentEntities = {item.get("name"): item.get("id") for item in entities}
        conn.close()
        return currentEntities
    except Exception as e:
        print e


################################
### Get list of new entities ###
################################
def getNewEntities():
    """
        Takes No Parameters
        Returns the list of entities in the config
    """
    print "Getting list of new entities"
    return [entity["name"] for entity in configData["entities"]]


#######################################
### Delete the entity with given id ###
#######################################
def deleteEntity(id):
    """
        Takes id as parameter
        Deletes the entity classifier with the id passed as parameter
    """
    try:
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("DELETE",
                     "/luis/api/v2.0/apps/{0}/versions/{1}/entities/{2}".format(configData["appID"],
                                                                                configData["activeVersion"], id),
                     None, headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except Exception as e:
        print e


######################################
### Create a new entity classifier ###
######################################
def createEntity(entity):
    """
        Takes the entity name as parameter
        Creates a new Entity Classifier with the given Entity Name
    """
    try:

        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("POST", "/luis/api/v2.0/apps/{0}/versions/{1}/entities".format(configData["appID"],
                                                                                    configData["activeVersion"]),
                     json.dumps({"Name": entity}),
                     headersWrite)
        response = conn.getresponse()
        conn.close()
        return response.status == 201
    except Exception as e:
        print e
