import json
import sys
import ast
import os
import httplib, urllib, base64


import app
import config
import intents
import entities


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
        
        #### Handle Intents #####

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

        #get list of intents to be created
        intents_to_create = set(new_intents) - set(current_intents)
        for intent in intents_to_create:
            createStatus = intents.createIntent(intent)
            if createStatus:
                print intent + " created."
            else:
                print "There was an error"


        ### Handle entities ###

        #get list of entities of the application
        current_entities = entities.getCurrentEntities(config_data['appID'])
        print "Current Entities: " + str(current_entities)

        #get list of new entities
        new_entities = entities.getNewEntities()
        print "New Entities: " + str(new_entities)

        #get list of entities missing in config 
        missing_entities = set(current_entities) - set(new_entities)
        for entity in missing_entities:
            print "Entity " + entity + " is missing in the config but is present on the model."
            answer = raw_input("Delete it? (Y/N):")
            if answer == 'Y' or answer == 'y':
                deleteStatus = entities.deleteEntity(current_entities[entity])
                if deleteStatus:
                    print entity + " deleted"
                else:
                    print "There was an error"

        #get list of entities to be created
        entities_to_create = set(new_entities) - set(current_entities)
        for entity in entities_to_create:
            createStatus = entities.createEntity(entity)
            if createStatus:
                print entity + " created."
            else:
                print "There was an error"



        
