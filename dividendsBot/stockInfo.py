import divInfo
import json
import utils

__cacheFileName = 'dividendsBotCache'

class stockInfo:
    def __init__(self, divInfo):
        self.ticker = divInfo.ticker
        self.div = divInfo
    def __eq__(self, other):
        return self.div == other.div
    def __hash__(self):
        return hash(self.div)
    def __str__(self):
        return self.name + '\t\t\t(' + self.ticker + ')\t' + str(self.isTinkoff) + '\t' + str(self.price) + '\t' + str(self.div.divPercents)

    div = divInfo.divInfo()
    ticker = ''
    name = ''
    price = 0
    isTinkoff = False
    
def decodeJsonToStockInfo(stockDict):
    stock = stockInfo(divInfo.decodeJsonToDivInfo(stockDict.get('div', {})))
    stock.ticker = stockDict.get('ticker', '')
    stock.name = stockDict.get('name', '')
    stock.price = int(stockDict.get('price', 0))
    stock.isTinkoff = bool(stockDict.get('isTinkoff', False))
    return stock

def loadCacheData():
    jsonStr = utils.loadJsonFile(__cacheFileName)
    jsonData = json.loads(jsonStr)
    stocks = []
    for stockDict in jsonData:
        stocks.append(decodeJsonToStockInfo(stockDict))
    return stocks
    
