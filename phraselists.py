import json
import sys
import ast
import os
import httplib, urllib, base64

import config

config_data = config.getConfig()

###############################################
### Get list of Phraselists of the Application ###
###############################################
def getExistingPhraselists(appID):
    """
        Takes appID as a parameter
        Returns the current Phraselists on the Application on the server
    """
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET","/luis/v1.0/prog/apps/{0}/phraselists?%{1}" .format(config_data["appID"], params),body_json, headers)

        print "Getting list of existing phraselists..."
        response = conn.getresponse()
        code = response.status
        if code == 200:
            current_phraselists = {}
            data = response.read()
            data = data.replace('true','1') #ast.literal_eval fails for booleans so replacing true with 1
            data = data.replace('false','0') #ast.literal_eval fails for booleans so replacing false with 0
            phraselists =  ast.literal_eval(data)
            for phraselist in phraselists:
                current_phraselists[phraselist['Name']] = {
                                                             "Id": phraselist['Id'],
                                                             "phrases":phraselist['Phrases']
                                                          }
            return current_phraselists
        else:
            return None
        conn.close()
    except Exception as e:
        print e


###################################
### get list of new phraselists ###
###################################
def getNewPhraselists():
    """
        Takes No Parameters
        Returns the list of phraselists in the config
    """
    new_phraselists = {}
    print "Getting list of new phraselists..."
    for phraselist in config_data["phraselists"]:
        new_phraselists[phraselist["name"]] = {
                                                "phrases" : phraselist['phrases'],
                                                "mode"    : phraselist['mode']
                                               }
    return new_phraselists


#######################################
### delete the phraselist with given id ###
#######################################
def deletePhraselist(phraselistID):
    """
        Takes phraselistID as parameter
        Deletes the phraselist with the phraselistID passed as parameter
    """
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    print "Deleting Phraselist..."

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("DELETE","/luis/v1.0/prog/apps/{0}/phraselists/{1}?{2}" .format(config_data["appID"], phraselistID, params),body_json, headers)
        response = conn.getresponse()
        code = response.status
        if code == 200:
            return True
        else:
            return False
    except Exception as e:
        print e
    
######################################
###    create a new Phraselist     ###
######################################
def createPhraselist(name,phrases,mode):
    """
        Takes the phraselist name and phraselist phrases as parameters
        Creates a new phraselist with the given Entity Name
    """
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body = {}
    body["Name"] = name
    body["Mode"] = mode
    body["Phrases"] = ",".join(phrases)

    body_json = json.dumps(body)

    print "Creating Phraselist for " + name + "..."

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST","/luis/v1.0/prog/apps/{0}/phraselists?%{1}" .format(config_data["appID"], params),body_json, headers)
        response = conn.getresponse()
        code = response.status
        if code == 201:
            return True
        else:
            return False
    except Exception as e:
        print e

###########################################
### update the phraselist with given id ###
###########################################
def updatePhraselist(phraselistID,phrases,mode,name):
    """
        Takes phraselistID as parameter
        Deletes the phraselist with the phraselistID passed as parameter
    """
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body = {}
    body["Name"] = name
    body["Mode"] = mode
    body["Phrases"] = ",".join(phrases)
    body["IsActive"] = True

    body_json = json.dumps(body)

    print "Updating " + name + "..."

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("PUT","/luis/v1.0/prog/apps/{0}/phraselists/{1}?{2}" .format(config_data["appID"], phraselistID, params),body_json, headers)
        response = conn.getresponse()
        code = response.status
        if code == 200:
            return True
        else:
            return False
    except Exception as e:
        print e