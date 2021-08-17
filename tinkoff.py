import tinvest
import time
import utils
#import datetime
#from dateutil.relativedelta import relativedelta

class tinkoff:
    def getStocks(self):
        try:
            stocks = self.__client.get_market_stocks();
            if stocks.status == 'Ok':
                return stocks.payload.instruments;
        except tinvest.TinvestError as err:
            utils.log('getStocks error: ' + err.response, self)
        return None

    def __getStock(self, ticker):
        try:
            stock = self.__client.get_market_search_by_ticker(ticker)
            if stock.status == 'Ok':
                if stock.payload.total > 1:
                    print('getStock multi stock: ' + ticker)
                if stock.payload.total >= 1:
                    return stock.payload.instruments[0];
                return -1
        except tinvest.TinvestError as err:
            utils.log('getStocks error: ' + err.response, self)
        return None

    def getStock(self, ticker):
        stock = tinkoff.__getStock(self, ticker)
        while not stock:
            sleep(10)
            stock = tinkoff.__getStock(self, ticker)
        if stock == -1:
            return None
        return stock

    #to = datetime.datetime.now(datetime.timezone.utc)
    #from_ = to - relativedelta(months=1)
    #.iso_format()

    __TOKEN = "t.3AVYcoRFiwegFJxOxhgrXEV5Hhuq86jVmqRcJETCxY8Ee8CuTGhj4ABuhS37gnAuM2bcbBhtU1fvb-q2TGs_IA"
    __client = tinvest.SyncClient(token = __TOKEN, use_sandbox = True);
