import json
import os

CATALOG_DIR = "catalog/"

def loadData():
    if not os.path.exists(CATALOG_DIR + 'guilds.jsonl'):
        return 4, None

    with open(CATALOG_DIR + "data.json") as reader:
        if reader == None:
            reader = {}
        data = json.load(reader)
    return None, data

def saveData(data):
   with open(CATALOG_DIR + "data.json", "w") as writer:
       writer.write(json.dumps(data))