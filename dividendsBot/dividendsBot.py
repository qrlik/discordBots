import tinkoff
import yahoo
import seekingAlpha
import stockInfo
import utils

class dividendsBot:
    def __init__(self):
        data = utils.loadJsonFile(self.__cacheFileName)
        lastPostedId = int(data.get('lastPostedId', 0))
        
    __cacheFileName = 'dividendsBotCache'
    lastPostedId = 0

def main():
    bot = dividendsBot()
    divStocks = seekingAlpha.parseDivs()
    ti = tinkoff.tinkoff()
    stocks = []
    for divInfo in divStocks:
        if divInfo.id == bot.lastPostedId:
            break

        stock = stockInfo.stockInfo(divInfo)

        if ti.getStock(stock.ticker):
            stock.isTinkoff = True
        stockNameAndPrice = yahoo.getStockNameAndPrice(stock.ticker)
        if not stockNameAndPrice:
            continue
        stock.name = stockNameAndPrice[0]
        stock.price = stockNameAndPrice[1]
        stock.div.divPercents = round(stock.div.amount / stock.price * 100, 2);
        stocks.append(stock)

    #post messages in discord

    utils.saveJsonFile(__cacheFileName, {'lastPostedId': bot.lastPostedId})


if __name__ == '__main__':
    main()