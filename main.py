import json
import sys
import ast
import os
import httplib, urllib, base64


import app
import config
import intents


if __name__ == "__main__":
    config_data = config.getConfig()
    
    #create a new application if appId is None
    if config_data["appID"] == "None":
        app.createApp()

    #else check if the app exists and if not create it
    else:
        application = app.getApplication(config_data['appID'])
        if application:
            print "Application Found"
        else:
            print "No application with that ID exists"
            answer = raw_input("Create New Application? (Y/N):")
            if answer == 'Y' or answer == 'y':
                app.createApp()
                application = app.getApplication(config_data['appID'])
            else:
                print "Cancelled"

    if application:
        
        #get list of intents of the application
        current_intents = intents.getCurrentIntents(config_data['appID'])
        
        print "Current Intents: "  + str(current_intents)

        #get list of new intents 
        new_intents = intents.getNewIntents()

        print "New Intents: " + str(new_intents)

        #get list of intents missing in config 
        missing_intents = set(current_intents) - set(new_intents)
        for intent in missing_intents:
            print "Intent " + intent + " is missing in your config but is present on the model."
            answer = raw_input("Delete it? (Y/N):")
            if answer == 'Y' or answer == 'y':
                deleteStatus = intents.deleteIntent(current_intents[intent])
                if deleteStatus:
                    print intent + " deleted"
                else:
                    print "There was an error"
        
