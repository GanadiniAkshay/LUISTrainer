import json
import sys
import ast
import os
import httplib, urllib, base64


import config


config_data = config.getConfig()

##################################
####  create new application #####
##################################
def createApp():
    """
        Takes No Parameters
        Creates a new Application and adds the appID into config.json
    """
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key':config_data["subscription_key"]
    }

    params = urllib.urlencode({})

    body = {}

    body["Name"] = config_data["name"]
    body["Description"] = config_data["description"]
    body["Culture"] = config_data["culture"]

    body_json = json.dumps(body)
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST","/luis/v1.0/prog/apps?%s" % params, body_json, headers)

        print "Creating Application...."
        response = conn.getresponse()
        data = response.read()
        print(data)
        print "Application Created"
        config_data['appID'] = data.replace('\"','')
        config.updateConfig(config_data)
        conn.close()
    except Exception as e:
        print e

###########################################
### get the application with a given id ###
###########################################
def getApplication(appID):
    """
        Takes appID as parameter
        Returns the application with the ID passed in the parameter
    """
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET","/luis/v1.0/prog/apps/{0}?%{1}" .format(config_data["appID"], params),body_json, headers)

        print "Checking if application exists..."
        response = conn.getresponse()
        code = response.status
        if code == 200:
            return True
        else:
            return False
        conn.close()
    except Exception as e:
        print e