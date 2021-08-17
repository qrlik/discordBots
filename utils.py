import datetime
import json
import os.path

def loadJsonFile(filename):
    try:
        with open(filename + '.json') as infile:
            return json.load(infile)
    except:
        return None

def saveJsonFile(filename, data):
    with open(filename + '.json', 'w') as outfile:
        json.dump(data, outfile)

def log(error, obj = None):
    source = '' if not obj else type(obj).__name__
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    logStr = now + ': ' + source + ': ' + error + '\n'
    print(logStr)
    
    file = 'Logs.txt'
    mode = 'a' if os.path.exists(file) else 'x'
    with open(file, mode) as f:
        f.write(logStr)