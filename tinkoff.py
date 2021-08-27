import os
import tinvest
import asyncio
import time
import utils
#import datetime
#from dateutil.relativedelta import relativedelta

__TOKEN = os.getenv('TINVEST_SANDBOX_TOKEN')
__client = tinvest.SyncClient(token = __TOKEN, use_sandbox = True);

def __getStock(ticker):
    try:
        stock = __client.get_market_search_by_ticker(ticker)
        if stock.status == 'Ok':
            if stock.payload.total > 1:
                print('tinkoff:getStock multi stock: ' + ticker)
            if stock.payload.total >= 1:
                return stock.payload.instruments[0];
            return -1
    except Exception as err:
        utils.log('tinkoff:getStocks error: ' + str(err))
    return None

async def getStocks(tickers):
    result = {}
    counter = 0
    for ticker, value in tickers.items():
        if counter >= 75:
            print('SLEEP\n\n\n\n')
            counter = 0
            await asyncio.sleep(10)
        print('send '+ ticker + '\n')
        counter += 1
        searchResult = await getStock(ticker)
        if searchResult:
            result.setdefault(ticker, value)
    return result

async def getStock(ticker):
    stock = __getStock(ticker)
    while not stock:
        await asyncio.sleep(3)
        stock = __getStock(ticker)
    if stock == -1:
        return None
    return stock

#to = datetime.datetime.now(datetime.timezone.utc)
#from_ = to - relativedelta(months=1)
#.iso_format()

