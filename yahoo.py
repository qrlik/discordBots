import json
import requests
import asyncio
import aiohttp
import utils
from enum import Enum

__API_URL = 'https://query2.finance.yahoo.com/'
__SUMMARY = 'v10/finance/quoteSummary/'
__MODULES = '?modules='

__headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
              'Accept-Language': 'en-US',
              'Referer': 'http://www.google.com/',
              'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
__session = requests.Session() 
__session.headers.update(__headers)

class eModule(Enum):
    PRICE = 1
    FINANCIAL = 2
    STATISTIC = 3

moduleDict = {eModule.PRICE: 'price',
              eModule.FINANCIAL: 'financialData',
              eModule.STATISTIC: 'defaultKeyStatistics'}

def __getRequestUrl(ticker, module):
    return __API_URL + __SUMMARY + ticker + __MODULES + module

def __checkTicker(ticker):
    return ticker.replace('.', '-')

def __getStockNameAndPrice(ticker):
    try:
        url = __getRequestUrl(ticker, moduleDict[eModule.PRICE])
        response = __session.get(url)
        if response.ok:
            price = response.json()['quoteSummary']['result'][0]['price']
            if not price['regularMarketPrice'].get('raw'):
                return -1
            name = price['longName'] if price['longName'] else price['shortName']
            return (name, price['regularMarketPrice']['raw'])
        else:
            utils.log('yahoo:__getStockNameAndPrice ' + ticker + ' reason ' + response.reason)
            if 'Not Found' not in response.reason:
                return None
    except Exception as e:
        utils.log('yahoo:__getStockNameAndPrice request error: ' + str(e))
    return -1

async def getStockNameAndPrice(ticker):
    ticker = __checkTicker(ticker)
    data = __getStockNameAndPrice(ticker)
    while not data:
        await asyncio.sleep(3)
        data = __getStockNameAndPrice(ticker)
    if data == -1:
        return None
    return data

#assetProfile
#incomeStatementHistory
#incomeStatementHistoryQuarterly
#balanceSheetHistory
#balanceSheetHistoryQuarterly
#cashflowStatementHistory
#cashflowStatementHistoryQuarterly
#defaultKeyStatistics
#financialData
#calendarEvents
#secFilings
#recommendationTrend
#upgradeDowngradeHistory
#institutionOwnership
#fundOwnership
#majorDirectHolders
#majorHoldersBreakdown
#insiderTransactions
#insiderHolders
#netSharePurchaseActivity
#earnings
#earningsHistory
#earningsTrend
#industryTrend
#indexTrend
#sectorTrend