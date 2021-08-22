import json
import requests
import asyncio
import utils
from enum import Enum

__API_URL = 'https://query2.finance.yahoo.com/'
__SUMMARY = 'v10/finance/quoteSummary/'
__MODULES = '?modules='

__session = requests.Session() 
__session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' })

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
    except requests.exceptions.RequestException as e:
        utils.log('yahoo:__getStockNameAndPrice request error: ' + str(e))
    return -1

def __getStockFloat(ticker):
    try:
        url = __getRequestUrl(ticker, moduleDict[eModule.STATISTIC])
        response = __session.get(url)
        if response.ok:
            stats = response.json()['quoteSummary']['result'][0]['defaultKeyStatistics']
            if not stats.get('floatShares') or not stats['floatShares'].get('raw'):
                return -1
            return stats['floatShares']['raw']
        else:
            utils.log('yahoo:__getStockFloat ' + ticker + ' reason ' + response.reason)
            if 'Not Found' not in response.reason:
                return None
    except requests.exceptions.RequestException as e:
        utils.log('yahoo:__getStockFloat request error: ' + str(e))
    return -1

async def getStockNameAndPrice(ticker):
    ticker = __checkTicker(ticker)
    data = __getStockNameAndPrice(ticker)
    while not data:
        await asyncio.sleep(10)
        data = __getStockNameAndPrice(ticker)
    if data == -1:
        return None
    return data

async def getStockFreeFloat(ticker):
    ticker = __checkTicker(ticker)
    data = __getStockFloat(ticker)
    while not data:
        await asyncio.sleep(10)
        data = __getStockFloat(ticker)
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