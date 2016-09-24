import json
import sys
import ast
import os
import httplib, urllib, base64

import config

config_data = config.getConfig()


##################################
### Get list of all utterances ###
##################################
def getUtterances():
    """
        Takes no parameters
        Gets all the utterances for a given app
    """
    utterance_ids = []
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("GET","/luis/v1.0/prog/apps/{0}/examples?skip=0&count=100000000000%{1}" .format(config_data["appID"],params),body_json, headers)

        print "Getting list of utterances..."
        response = conn.getresponse()
        code = response.status
        if code == 200:
            data = response.read()
            data = data.replace('true','1')
            data = data.replace('false','0')
            data = data.replace('null','-1')
            utterances = ast.literal_eval(data)
            for utterance in utterances:
                utterance_ids.append(utterance['exampleId'])
            return utterance_ids
        else:
            return None
        conn.close()
    except Exception as e:
        print e


####################################
### Delete utterance of given id ###
####################################
def deleteUtterance(id):
    """
        Takes exampleID as input
        Delete the utterances with given id
    """
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps({})

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("DELETE","/luis/v1.0/prog/apps/{0}/examples/{1}?%{2}" .format(config_data["appID"],id,params),body_json, headers)

        response = conn.getresponse()
        code = response.status
        if code == 200:
            return True
        else:
            return False
        conn.close()
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
    print "Getting list of new utterances..."

    #get list of entities from config
    config_entites = []
    for entity in config_data["entities"]:
        config_entites.append(entity["name"])
    
    utterances = []

    basePath = "./intents/"
    for subdirs, dirs, files in os.walk(basePath):
        for file in files:
            filepath = subdirs + os.sep + file
            if filepath.endswith(".txt"):
                intent = filepath.split('/')[-1].split('.')[0]
                print "Adding examples for intent " + intent
                with open(filepath,'r') as intentFile:
                    for example in intentFile:
                        utterance = {}
                        entityLabels = []

                        #check if example has entities
                        example_split = example.split("<=>")

                        example_text = example_split[0]
            
                        if len(example_split) > 1:
                            example_entities = example_split[1:]

                            # check if entities mentioned in text exist in config
                            for example_entity in example_entities:
                                if not example_entity.strip() in config_entites:
                                    print "The entity " + example_entity + " used in " + example_text + " is not present in config."
                                    return None

                            # check if parantheses match
                            open_paran_count = example_text.count('(')
                            close_paran_count = example_text.count(')')

                            if open_paran_count != close_paran_count:
                                print "Paranthesis don't match for " + example_text
                                return None
                            
                            #check if paranthesis and provide entities match
                            if open_paran_count != len(example_entities):
                                print "The entities provided and the words marked in paranthesis don't match for " + example_text
                                return None

                            start_pos = 0
                            entities_count = 0
                            no_of_entities = len(example_entities)

                            while entities_count<no_of_entities:
                                start_pos = example_text.find('(',start_pos,len(example_text))+1
                                end_pos   = example_text.find(')',start_pos,len(example_text))-1

                                entityLabel = {}

                                entityLabel["EntityType"] = example_entities[entities_count].strip()
                                entityLabel["StartToken"] = start_pos - ((entities_count * 2 ) + 1)
                                entityLabel["EndToken"]   = end_pos - ((entities_count *2 ) + 1)

                                entities_count += 1

                                entityLabels.append(entityLabel)
 
                        
                        utterance["ExampleText"] = example_text.replace('(','').replace(')','')
                        utterance["SelectedIntentName"] = intent
                        utterance["EntityLabels"] = entityLabels

                        # #check for entities
                        # entityLabels = []
                        # example_split = example.split(" <=> ")
                        # if len(example_split) > 1:
                        #     example_utterance = example_split[0]
                        #     entityStartLabel = example_utterance.find('(') + 1
                        #     entityEndLabel   = example_utterance.find(')') - 1
                        #     example = example_utterance.replace('(','')
                        #     example = example_utterance.replace(')','')
                        #     entityLabel = {}
                        #     entityLabel["EntityType"] = example_split[1]
                        #     entityLabel["StartToken"] = entityStartLabel
                        #     entityLabel["EndToken"] = entityEndLabel

                        #     entityLabels.append(entityLabel)
                        # utterance["ExampleText"] = example
                        # utterance["SelectedIntentName"] = intent
                        # utterance["EntityLabels"] = entityLabels

                        utterances.append(utterance)
    headers = {
        #Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key':config_data['subscription_key']
    }

    params = urllib.urlencode({})

    body_json = json.dumps(utterances)

    print body_json

    try:
        conn = httplib.HTTPSConnection("api.projectoxford.ai")
        conn.request("POST","/luis/v1.0/prog/apps/{0}/examples?%{1}" .format(config_data["appID"],params),body_json, headers)

        response = conn.getresponse()
        code = response.status
        if code == 201:
            return True
        else:
            return False
        conn.close()
    except Exception as e:
        print e

