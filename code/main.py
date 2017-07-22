import app
import config
import entities
import intents
import phraselists
import train
import utterances

if __name__ == "__main__":
    configData = config.getConfig()

    if configData["appID"] == "None":
        app.createApp()
    else:
        application = app.getApplication()
        if application:
            print "Application Found"
        else:
            print "No application with that ID exists"
            if raw_input("Create New Application? (Y/N):").lower() == "y":
                app.createApp()
                application = app.getApplication()
            else:
                print "Cancelled"

    if application:
        #### Handle Intents #####

        # Get list of existing intents of the application
        existingIntents = intents.getExistingIntents()
        existingIntentsSet = set(existingIntents) if existingIntents is not None else set()

        # Get list of new intents
        newIntents = intents.getNewIntents()
        newIntentsSet = set(newIntents) if newIntents is not None else set()

        # Get list of intents missing in config
        missingIntents = existingIntentsSet - newIntentsSet
        for intent in missingIntents:
            if intent != "None":
                print "Intent " + intent + " is missing in your config, but is present on the model"
                if raw_input("Delete it? (Y/N):").lower() == "y":
                    if not intents.deleteIntent(existingIntents[intent]):
                        print "There was an error trying to delete " + intent

        # Get list of intents to be created
        intentsToCreate = newIntentsSet - existingIntentsSet
        for intent in intentsToCreate:
            success = intents.createIntent(intent)
            if not success:
                print "There was an error trying to create " + intent

        ### Handle entities ###

        # Get list of existing entities of the application
        existingEntities = entities.getExistingEntities()
        existingEntitiesSet = set(existingEntities) if existingEntities is not None else set()

        # Get list of new entities
        newEntities = entities.getNewEntities()
        newEntitiesSet = set(newEntities) if newEntities is not None else set()

        # Get list of entities missing in config
        missingEntities = existingEntitiesSet - newEntitiesSet
        for entity in missingEntities:
            print "Entity " + entity + " is missing in the config, but is present on the model"
            if raw_input("Delete it? (Y/N):").lower() == "y":
                if not entities.deleteEntity(existingEntities[entity]):
                    print "There was an error trying to delete " + entity

        # Get list of entities to be created
        entitiesToCreate = newEntitiesSet - existingEntitiesSet
        for entity in entitiesToCreate:
            if not entities.createEntity(entity):
                print "There was an error trying to create " + entity + " (might be a prebuilt)"

        ### Handle phraselists ###

        # Get list of existing phraselists of the application
        existingPhraselist = phraselists.getExistingPhraselists()
        existingPhraselistsSet = set(existingPhraselist) if existingPhraselist is not None else set()

        # Get list of new phraselists
        newPhraselists = phraselists.getNewPhraselists()
        newPhraselistsSet = set(newPhraselists) if newPhraselists is not None else set()

        # Get list of phraselists missing in config
        missingPhraselists = existingPhraselistsSet - newPhraselistsSet
        for phraselist in missingPhraselists:
            print "Phraselist " + phraselist + " is missing in the config but is present on the model"
            if raw_input("Delete it? (Y/N):").lower() == "y":
                if not phraselists.deletePhraselist(existingPhraselist[phraselist]["Id"]):
                    print "There was an error trying to delete " + phraselist

        # Get list of phraselists to be created
        phraselistsToCreate = newPhraselistsSet - existingPhraselistsSet
        for phraselist in phraselistsToCreate:
            if not phraselists.createPhraselist(phraselist, newPhraselists[phraselist]["phrases"],
                                                newPhraselists[phraselist]["mode"]):
                print "There was an error trying to create " + phraselist

        # Get list of phraselists to be updated
        phraselistsToUpdate = newPhraselistsSet.intersection(existingPhraselistsSet)
        flag = 0
        print "Checking if updates needed to phraselists"
        for phraselist in phraselistsToUpdate:
            oldPhrases = set(existingPhraselist[phraselist]["phrases"].split(","))
            newPhrases = set(newPhraselists[phraselist]["phrases"])
            if oldPhrases != newPhrases:
                if not phraselists.updatePhraselist(existingPhraselist[phraselist]["Id"],
                                                    newPhraselists[phraselist]["phrases"]
                        , newPhraselists[phraselist]["mode"], phraselist):
                    print "There was an error trying to update " + phraselist
                flag = 1
        if flag == 0:
            print "No phraselist needs updates"

        ##### Handle Utterances ####

        # Get utterance id of existing utterances
        utteranceIds = utterances.getUtterances()

        # Delete the existing utterances
        print "Deleting existing utterances"
        for id in utteranceIds:
            if utterances.deleteUtterance(id):
                continue
            else:
                print "There was an error trying to delete utterance " + id

        # Add new utterances
        print "Adding new utterances"
        if not utterances.addUtterances():
            print "There was an error trying to add new utterances"

        # Train the system
        trained = False
        i = 0
        while trained is False and ++i < 5:
            trained = train.train()
            print "Model successfully trained"

        if trained is False and i == 5:
            print "Model failed to be trained"
