import json

def loadJsonFile(filename):
    try:
        with open(filename + '.json') as infile:
            return json.load(infile)
    except:
        return None

def saveJsonFile(filename, data):
    with open(filename + '.json', 'w') as outfile:
        json.dump(data, outfile)