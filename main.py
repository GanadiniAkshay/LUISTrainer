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
        config_data['appID'] = data.replace('\"','')
        updateConfig()
        conn.close()
    except Exception as e:
        print e

#get the application with id
def getApplication(appID):
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET","/luis/v1.0/prog/apps/{0}?%{1}" .format(config_data["appID"], params),body_json, headers)
        response = conn.getresponse()
        code = response.status
        if code == 200:
            data = response.read()
            return data
        else:
            return None
        conn.close()
    except Exception as e:
        print e


if __name__ == "__main__":
    config_data = getConfig()
    
    #create a new application if appId is None
    if config_data["appID"] == "None":
        createApp()

    #else check if the app exists
    else:
        application = getApplication(config_data['appID'])
        if application:
            print application
        else:
            print "No application with that ID exists"
            answer = raw_input("Create New Application? (Y/N):")
            if answer == 'Y' or answer == 'y':
                createApp()
            else:
                print "Cancelled"
        
