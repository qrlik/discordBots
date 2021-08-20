import os
import tinvest
import time
import utils
#import datetime
#from dateutil.relativedelta import relativedelta

__TOKEN = os.getenv('TINVEST_SANDBOX_TOKEN')
__client = tinvest.SyncClient(token = __TOKEN, use_sandbox = True);

def getStocks():
    try:
        stocks = __client.get_market_stocks();
        if stocks.status == 'Ok':
            return stocks.payload.instruments;
    except tinvest.TinvestError as err:
        utils.log('tinkoff:getStocks error: ' + err.response)
    return None

def __getStock(ticker):
    try:
        stock = __client.get_market_search_by_ticker(ticker)
        if stock.status == 'Ok':
            if stock.payload.total > 1:
                print('getStock multi stock: ' + ticker)
            if stock.payload.total >= 1:
                return stock.payload.instruments[0];
            return -1
    except tinvest.TinvestError as err:
        utils.log('tinkoff:getStocks error: ' + err.response)
    return None

def getStock(ticker):
    stock = __getStock(ticker)
    while not stock:
        sleep(10)
        stock = __getStock(ticker)
    if stock == -1:
        return None
    return stock

#to = datetime.datetime.now(datetime.timezone.utc)
#from_ = to - relativedelta(months=1)
#.iso_format()

