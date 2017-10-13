import httplib
import json
import os

import config
import utils

configData = config.getConfig()
headers = {"Ocp-Apim-Subscription-Key": configData["subscription_key"], "Content-Type": "application/json"}


##################################
### Get list of all utterances ###
##################################
def getUtterances():
    """
        Takes no parameters
        Gets all the utterances for a given app
    """
    try:
        utteranceIds = None
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("GET",
                     "/luis/api/v2.0/apps/{0}/versions/{1}/examples?skip=0&count=100000000000".format(
                         configData["appID"], configData["activeVersion"]), None, headers)
        response = conn.getresponse()
        if response.status == 200:
            utterances = json.loads(response.read())
            utteranceIds = [utterance["id"] for utterance in utterances]
        conn.close()
        return utteranceIds
    except Exception as e:
        print e


####################################
### Delete utterance of given id ###
####################################
def deleteUtterance(id):
    """
        Takes id as parameter
        Delete the utterances with given id
    """
    try:
        conn = httplib.HTTPSConnection(configData["luisUrl"])
        conn.request("DELETE", "/luis/api/v2.0/apps/{0}/versions/{1}/examples/{2}".format(configData["appID"],
                                                                                          configData["activeVersion"],
                                                                                          id),
                     None, headers)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except Exception as e:
        print e


########################
### Add utterances   ###
########################
def addUtterances():
    """
        Takes no parameter
        Reads all the intent texts and creates the utterances and adds it to the application
    """
    configEntites = [entity["name"] for entity in configData["entities"]]
    basePath = "../intents/"
    result = True
    for subdirs, dirs, files in os.walk(basePath):
        for file in files:
            filepath = os.path.join(subdirs, file)
            if result and filepath.endswith(".txt"):
                utterances = []
                intent = os.path.splitext(file)[0]
                print "Adding utterances for " + intent
                with open(filepath, "r") as intentFile:
                    for example in intentFile:
                        entityLabels = []

                        # Check if example has entities
                        exampleSplit = example.strip().split("<=>")
                        exampleText = exampleSplit[0].strip()

                        if len(exampleSplit) > 1:
                            exampleEntities = exampleSplit[1:]

                            # check if entities mentioned in text exist in config
                            for exampleEntity in exampleEntities:
                                if not exampleEntity.strip() in configEntites:
                                    print "The entity " + exampleEntity + " used in " + exampleText + " is not present in config"
                                    return None

                            # Check if parantheses match
                            openParanCount = exampleText.count("(")
                            closeParanCount = exampleText.count(")")

                            if openParanCount != closeParanCount:
                                print "Paranthesis don't match for " + exampleText
                                return None

                            # Check if paranthesis and provide entities match
                            if openParanCount != len(exampleEntities):
                                print "The entities provided and the words marked in paranthesis don't match for " + exampleText
                                return None

                            startPos = 0
                            entitiesCount = 0
                            noOfEntities = len(exampleEntities)

                            while entitiesCount < noOfEntities:
                                startPos = exampleText.find("(", startPos, len(exampleText)) + 1
                                endPos = exampleText.find(")", startPos, len(exampleText)) - 1
                                entityLabel = {"EntityName": exampleEntities[entitiesCount].strip(),
                                               "StartCharIndex": startPos - ((entitiesCount * 2) + 1),
                                               "endCharIndex": endPos - ((entitiesCount * 2) + 1)}
                                entitiesCount += 1
                                entityLabels.append(entityLabel)

                            utterances.append({"Text": exampleText.replace("(", "").replace(")", ""),
                                               "IntentName": intent, "EntityLabels": entityLabels})

                if len(utterances) > 0:
                    result = True
                    for utters in utils.grouper(utterances, 100):
                        utters = [a for a in utters if a is not None]  # drop trailing Nones.
                        try:
                            conn = httplib.HTTPSConnection(configData["luisUrl"])
                            conn.request("POST", "/luis/api/v2.0/apps/{0}/versions/{1}/examples".format(
                                configData["appID"], configData["activeVersion"]), json.dumps(utters), headers)
                            response = conn.getresponse()
                            conn.close()
                            result = response.status == 201 and result
                        except Exception as e:
                            print e
                            result = False
    return result