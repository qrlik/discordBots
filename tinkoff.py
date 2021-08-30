import os
import tinvest
import asyncio
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
                utils.log('tinkoff:getStock multi stock: ' + ticker)
            if stock.payload.total >= 1:
                return stock.payload.instruments[0];
            return -1
    except Exception as err:
        utils.log('tinkoff:getStock error: ' + str(err))
    return None

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

