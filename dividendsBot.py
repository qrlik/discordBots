import tinkoff
import seekingAlpha
import yahoo

def main():
    price = yahoo.getStockPrice('CLOV')
    test = ''

    #divStocks = seekingAlpha.parseDivs()
    #ti = tinkoff.tinkoff()
    #tiDivStocks = []
    #for stock in divStocks:
    #    tiStockData = ti.getStock(stock.ticker) #while
    #    if not tiStockData:
    #        continue
    #    tiDivStocks.append(stock)
    #    price = ti.getStockPrice(tiStockData.figi)

if __name__ == '__main__':
    main()