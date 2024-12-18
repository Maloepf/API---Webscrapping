import os
import json

#define the path to kaggle.json
KAGGLE_JSON_PATH = os.path.join(os.path.dirname(__file__), 'kaggle.json')

#load the JSON data into a variable
with open(KAGGLE_JSON_PATH, 'r') as file:
    kaggle = json.load(file)
