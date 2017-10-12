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
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("POST", "/luis/api/v2.0/apps/{0}/versions/{1}/train".format(configData["appID"],
                                                                                 configData["activeVersion"]), None,
                     headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 202
    except Exception as e:
        print e
