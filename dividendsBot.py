import os
import tinvest
import datetime
from dateutil.relativedelta import relativedelta
import time
import seekingAlpha

TOKEN = "t.3AVYcoRFiwegFJxOxhgrXEV5Hhuq86jVmqRcJETCxY8Ee8CuTGhj4ABuhS37gnAuM2bcbBhtU1fvb-q2TGs_IA"

class tinkoff:
    def getStocks(self):
        try:
            stocks = self.client.get_market_stocks();
            if stocks.status == 'Ok':
                return stocks.payload.instruments;
            return None
        except tinvest.Error as err:
            print('getStocks error: ', err.response)
            return None

    def getStock(self, ticker):
        try:
            stock = self.client.get_market_search_by_ticker(ticker)
            if stock.status == 'Ok':
                if stock.payload.total == 1:
                    return stock.payload.instruments[0];
                elif stock.payload.total > 1:
                    print('getStock multi stock: ' + ticker)
            return None
        except tinvest.Error as err:
            print('getStock error: ', err.response)
            return None

    def getStockPrice(self, figi):
        try:
            to = datetime.datetime.now(datetime.timezone.utc)
            from_ = to - relativedelta(months=1)
            stock = self.client.get_market_candles(figi, from_.isoformat(), to.isoformat(), tinvest.CandleResolution.month)
            if stock.status == 'Ok' and len(stock.payload.candles) > 0:
                return stock.payload.candles.pop().c;
            return None
        except tinvest.Error as err:
            print('getStockPrice error: ', err.response)
            return None
        
    client = tinvest.SyncClient(token = TOKEN, use_sandbox = True);

def main():
    divStocks = seekingAlpha.parseDivs()
    ti = tinkoff()
    tiDivStocks = []
    for stock in divStocks:
        tiStockData = ti.getStock(stock.ticker)
        if not tiStockData:
            continue
        tiDivStocks.append(stock)
        price = ti.getStockPrice(tiStockData.figi)

if __name__ == '__main__':
    main()