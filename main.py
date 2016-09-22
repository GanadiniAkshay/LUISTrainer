import json
import sys
import ast
import os
import httplib, urllib, base64


import app
import config
import intents
import entities
import phraselists


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

        #get list of existing intents of the application
        existing_intents = intents.getExistingIntents(config_data['appID'])
        #print "Current Intents: "  + str(existing_intents)

        #get list of new intents 
        new_intents = intents.getNewIntents()
        #print "New Intents: " + str(new_intents)

        #get list of intents missing in config 
        missing_intents = set(existing_intents) - set(new_intents)
        for intent in missing_intents:
            print "Intent " + intent + " is missing in your config but is present on the model."
            answer = raw_input("Delete it? (Y/N):")
            if answer == 'Y' or answer == 'y':
                deleteStatus = intents.deleteIntent(existing_intents[intent])
                if deleteStatus:
                    print intent + " deleted"
                else:
                    print "There was an error"

        #get list of intents to be created
        intents_to_create = set(new_intents) - set(existing_intents)
        for intent in intents_to_create:
            createStatus = intents.createIntent(intent)
            if createStatus:
                print intent + " created."
            else:
                print "There was an error"


        ### Handle entities ###

        #get list of existing entities of the application
        existing_entities = entities.getExistingEntities(config_data['appID'])
        #print "Current Entities: " + str(existing_entities)

        #get list of new entities
        new_entities = entities.getNewEntities()
        #print "New Entities: " + str(new_entities)

        #get list of entities missing in config 
        missing_entities = set(existing_entities) - set(new_entities)
        for entity in missing_entities:
            print "Entity " + entity + " is missing in the config but is present on the model."
            answer = raw_input("Delete it? (Y/N):")
            if answer == 'Y' or answer == 'y':
                deleteStatus = entities.deleteEntity(existing_entities[entity])
                if deleteStatus:
                    print entity + " deleted"
                else:
                    print "There was an error"

        #get list of entities to be created
        entities_to_create = set(new_entities) - set(existing_entities)
        for entity in entities_to_create:
            createStatus = entities.createEntity(entity)
            if createStatus:
                print entity + " created."
            else:
                print "There was an error"


        ### Handle phraselists ###

        #get list of existing phraselists of the application
        existing_phraselists = phraselists.getExistingPhraselists(config_data['appID'])
        #print "Existing Phraselists: " + str(existing_phraselists)

        #get list of new phraselists
        new_phraselists = phraselists.getNewPhraselists()
        #print "New Phraselists: " + str(new_phraselists)

        #get list of phraselists missing in config 
        missing_phraselists = set(existing_phraselists) - set(new_phraselists)
        for phraselist in missing_phraselists:
            print "Phraselist " + phraselist + " is missing in the config but is present on the model."
            answer = raw_input("Delete it? (Y/N):")
            if answer == 'Y' or answer == 'y':
                deleteStatus = phraselists.deletePhraselist(existing_phraselists[phraselist]['Id'])
                if deleteStatus:
                    print phraselist + " deleted"
                else:
                    print "There was an error"

        #get list of phraselists to be created
        phraselists_to_create = set(new_phraselists) - set(existing_phraselists)
        for phraselist in phraselists_to_create:
            createStatus = phraselists.createPhraselist(phraselist,new_phraselists[phraselist]['phrases'],new_phraselists[phraselist]['mode'])
            if createStatus:
                print phraselist + " created."
            else:
                print "There was an error"

        #get list of phraselists to be updated
        phraselists_to_update = set(new_phraselists).intersection(set(existing_phraselists))
        flag = 0
        print "Checking if updates needed to phraselists..."
        for phraselist in phraselists_to_update:
            old_phrases = set(existing_phraselists[phraselist]['phrases'].split(","))
            new_phrases = set(new_phraselists[phraselist]["phrases"])
            if old_phrases != new_phrases:
                updateStatus = phraselists.updatePhraselist(existing_phraselists[phraselist]['Id'],new_phraselists[phraselist]['phrases']
                                                                ,new_phraselists[phraselist]['mode'],phraselist)
                if updateStatus:
                    print phraselist + " updated"
                else:
                    print "There was an error"
                flag = 1
        if flag == 0:
            print "No phraselist needs updates"




        
