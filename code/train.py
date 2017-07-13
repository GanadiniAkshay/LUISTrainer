import httplib

import config

configData = config.getConfig()
headers = {"Ocp-Apim-Subscription-Key": configData["subscription_key"]}


#############################
### Train the application ###
#############################
def train():
    """
        Takes No Parameter
        trains the LUIS Model
    """
    print "Training the LUIS Model"
    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("POST", "/luis/v1.0/prog/apps/{0}/train".format(configData["appID"]), None,
                     headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 202
    except Exception as e:
        print e
