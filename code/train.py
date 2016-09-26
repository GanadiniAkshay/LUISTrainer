import json
import sys
import ast
import os
import httplib, urllib, base64

import config

config_data = config.getConfig()

#############################
### Train the application ###
#############################
def train():
    """
        Takes No Parameter
        trains the LUIS Model
    """
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("POST","/luis/v1.0/prog/apps/{0}/train?%{1}" .format(config_data["appID"], params),body_json, headers)

        print "Training the LUIS Model..."
        response = conn.getresponse()
        code = response.status
        if code == 202:
            return True
        else:
            return False
        conn.close()
    except Exception as e:
        print e