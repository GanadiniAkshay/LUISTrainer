import json


#####################################################
### load the config file into a dictionary object ###
#####################################################
def getConfig():
    """ 
        Takes No Parameters
        Loads the config.json file into a json object and returns it
    """
    with open('../config.json') as config:
        data = json.load(config)

    return data


#############################
### update the cofig file ###
#############################
def updateConfig(data):
    """
        Takes data to write to config.json
        Updates the config file
    """
    print "Updating Config File"
    with open('../config.json', 'w') as config:
        json.dump(data, config)
    print "Updated Config File"
