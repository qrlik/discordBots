import datetime
import json
import os.path
from itertools import islice

def loadJsonFile(filename):
    try:
        with open(filename + '.json') as infile:
            return json.load(infile)
    except Exception as e:
        print('utils: loadJsonFile: ' + str(e))
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

def splitDict(data, size):
    splitResult = []
    it = iter(data)
    for i in range(0, len(data), size):
        splitResult.append({k:data[k] for k in islice(it, size)})
    return splitResult