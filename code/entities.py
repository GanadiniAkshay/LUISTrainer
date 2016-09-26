import json
import sys
import ast
import os
import httplib, urllib, base64

import config

config_data = config.getConfig()

###############################################
### Get list of Entities of the Application ###
###############################################
def getExistingEntities(appID):
    """
        Takes appID as a parameter
        Returns the current Entities on the Application on the server
    """
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET","/luis/v1.0/prog/apps/{0}/entities?%{1}" .format(config_data["appID"], params),body_json, headers)

        print "Getting list of existing entities..."
        response = conn.getresponse()
        code = response.status
        if code == 200:
            current_entities = {}
            data = response.read()
            entities = ast.literal_eval(data)
            for entity in entities:
                current_entities[entity['name']] = entity['id']
            return current_entities
        else:
            return None
        conn.close()
    except Exception as e:
        print e


################################
### get list of new entities ###
################################
def getNewEntities():
    """
        Takes No Parameters
        Returns the list of entities in the config
    """
    new_entities = []
    print "Getting list of new entities"
    for entity in config_data["entities"]:
        new_entities.append(entity["name"])
    return new_entities


#######################################
### delete the entity with given id ###
#######################################
def deleteEntity(entityID):
    """
        Takes entityID as parameter
        Deletes the entity classifier with the entityID passed as parameter
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
        conn.request("DELETE","/luis/v1.0/prog/apps/{0}/entities/{1}?{2}" .format(config_data["appID"], entityID, params),body_json, headers)
        response = conn.getresponse()
        code = response.status
        if code == 200:
            return True
        else:
            return False
    except Exception as e:
        print e
    
######################################
### create a new entity classifier ###
######################################
def createEntity(entity):
    """
        Takes the entity name as parameter
        Creates a new Entity Classifier with the given Entity Name
    """
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body = {}
    body["Name"] = entity

    body_json = json.dumps(body)

    print "Creating Entity Classifier for " + entity + "..."

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST","/luis/v1.0/prog/apps/{0}/entities?%{1}" .format(config_data["appID"], params),body_json, headers)
        response = conn.getresponse()
        code = response.status
        if code == 201:
            return True
        else:
            return False
    except Exception as e:
        print e