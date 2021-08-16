import tinkoff
import yahoo
import seekingAlpha
import stockInfo

def main():
    stocks = stockInfo.loadCacheData()
    divStocks = seekingAlpha.parseDivs()
    ti = tinkoff.tinkoff()
    for divInfo in divStocks:
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

    #stocksJson = json.dumps(stocks, default=lambda x: x.__dict__)
    #utils.saveJsonFile(__cacheFileName, stocksJson)

if __name__ == '__main__':
    main()