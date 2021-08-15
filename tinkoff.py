import tinvest
import datetime
from dateutil.relativedelta import relativedelta

class tinkoff:
    def getStocks(self):
        try:
            stocks = self.client.get_market_stocks();
            if stocks.status == 'Ok':
                return stocks.payload.instruments;
            else:
                return None
        except tinvest.Error as err:
            print('getStocks error: ', err.response)
        return -1

    def getStock(self, ticker):
        try:
            stock = self.client.get_market_search_by_ticker(ticker)
            if stock.status == 'Ok':
                if stock.payload.total > 1:
                    print('getStock multi stock: ' + ticker)
                if stock.payload.total >= 1:
                    return stock.payload.instruments[0];
            else:
                return None
        except tinvest.Error as err:
            print('getStock error: ', err.response)
        return -1

    __TOKEN = "t.3AVYcoRFiwegFJxOxhgrXEV5Hhuq86jVmqRcJETCxY8Ee8CuTGhj4ABuhS37gnAuM2bcbBhtU1fvb-q2TGs_IA"
    __client = tinvest.SyncClient(token = __TOKEN, use_sandbox = True);
