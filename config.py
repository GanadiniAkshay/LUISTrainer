import json
import sys
import ast
import os

#####################################################
### load the config file into a dictionary object ###
#####################################################
def getConfig():
    """ 
        Takes No Parameters
        Loads the config.json file into a json object and returns it
    """
    with open('config.json') as config_file:
        config_data = json.load(config_file)

    return config_data

#############################
### update the cofig file ###
#############################
def updateConfig():
    """
        Takes No Parameter
        Updates the config file with the app ID
    """
    print "Updating Config File..."
    with open('config.json','w') as config_file:
        json.dump(config_data,config_file)
    print "Updated Config File"