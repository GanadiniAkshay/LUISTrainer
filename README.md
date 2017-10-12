## LUIS Trainer

### A Simple python framework to train and build LUIS Models

#### Description
Creating and training LUIS models on the [website] (www.luis.ai) can be **slow and frustrating**.   
Instead you can use this framework which uses the LUIS API to train your models in a much simpler, meta-data driven way.

#### Usage
1. Setup Config
   * Add your subscription_key in config.json (Programmatic key for LUIS. You can find your's [here] (https://www.luis.ai/user/settings)
   * Add your App Name, App Description and appID. (LUIS app name and appId)  
     If it's a new app and you don't have an id, put appId as **None**

2. Create Intents
   * To create a intent just create a .txt file in the intents folder with the filename as the name of the intent.  
     You can add all the utterances or examples for this intent in this .txt, each on a seperate line.

3. Create Entities
   * To create a entity add a json object to the array of the entities field in the config.json file
     with the following schema  
     { "name" : _name of entity_}
   * To add the entity to a training example, put paranthesis around the example and then list   
     the entity names after the example seperated by '<=>'  
     eg: "Book a (Delta) flight from (NYC) to (Miami) <=> airlines <=> destination <=> destination"
         
        The order of entity names should be in the order in which they occur in the statement.
   
    **Note: Currently it doesn't work for hierarchial or composite entities.**

4. Create Phraselists
    * To create a phraselist add a json object to the array of the phraselists field in config.json file
      with the following schema  
      {   
          "name" : _name of phraselist_ ,  
          "mode" : _exchangable_ or _non-exchangable_,  
          "phrases" : [_comma seperated strings of phrases_]  
      }
  
5. Train/Build the LUIS Model
    * CD into code folder and run main.py ($ python main.py)
    
  After following the above steps, you can visit the application portal and you will find your application built and trained.
  
  You can keep making changes to your intent files/ entities/ phraselists any number of times you want. Just run main.py and your 
  model will be retrained with the changes.
  
#### Contributing
Feel free to report bugs, issues or send in pull requests.

#### License
MIT License
 
