import json
import sys
import httplib, urllib, base64

#declare global variables
config_data = {}

#load the config file into a dictionary object
def getConfig():
    with open('config.json') as config_file:
        config_data = json.load(config_file)

    return config_data

#update the cofig file
def updateConfig():
    print "Updating Config File..."
    with open('config.json','w') as config_file:
        json.dump(config_data,config_file)
    print "Updated Config File"

#create new application
def createApp():
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
        config_data['appID'] = data
        updateConfig()
    except Exception as e:
        print e


if __name__ == "__main__":
    config_data = getConfig()
    
    #create a new application if appId is None
    if config_data["appID"] == "None":
        createApp()

    #else check if the app exists
    else:
        print config_data["appID"]
