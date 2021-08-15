import tinkoff
import seekingAlpha
import yahoo

class stockInfo:
    def __init__(self, divInfo):
        self.ticker = divInfo.ticker
        self.div = divInfo
    def __str__(self):
        return self.name + '\t\t\t(' + self.ticker + ')\t' + str(self.isTinkoff) + '\t' + str(self.price) + '\t' + str(self.div.divPercents)
    div = seekingAlpha.divInfo()
    ticker = ''
    name = ''
    price = 0
    isTinkoff = False

def main():
    divStocks = seekingAlpha.parseDivs()
    ti = tinkoff.tinkoff()
    stocks = []
    for divInfo in divStocks:
        stock = stockInfo(divInfo)
        if ti.getStock(stock.ticker):
            stock.isTinkoff = True
        stockNameAndPrice = yahoo.getStockNameAndPrice(stock.ticker)
        stock.name = stockNameAndPrice[0]
        stock.price = stockNameAndPrice[1]
        stock.div.divPercents = round(stock.div.amount / stock.price * 100, 2);
        stocks.append(stock)

    for stock in stocks:
        print(stock)

if __name__ == '__main__':
    main()