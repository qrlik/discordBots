import json
import requests
import asyncio
import aiohttp
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
    except Exception as e:
        utils.log('yahoo:__getStockNameAndPrice request error: ' + str(e))
    return -1

async def __getStocksFloat(tickers):
    result = {}
    async with aiohttp.ClientSession() as session:
        for ticker in tickers:
            while True:
                try:
                    async with session.get(__getRequestUrl(ticker, moduleDict[eModule.STATISTIC])) as response:
                        if response.ok:
                            js = await response.json()
                            if not js['quoteSummary']['result']:
                                result.setdefault(ticker, 'N/A')
                            else:
                                stats = js['quoteSummary']['result'][0]['defaultKeyStatistics']
                                if not stats.get('floatShares') or not stats['floatShares'].get('raw'):
                                    result.setdefault(ticker, 'N/A')
                                else:
                                    result.setdefault(ticker, stats['floatShares']['raw'])
                            break
                        elif 'Not Found' not in response.reason:
                            await asyncio.sleep(3)
                        else:
                            break
                except Exception as e:
                    utils.log('yahoo:__getStockFloat request error: ' + str(e))
    return result

async def getStockNameAndPrice(ticker):
    ticker = __checkTicker(ticker)
    data = __getStockNameAndPrice(ticker)
    while not data:
        await asyncio.sleep(3)
        data = __getStockNameAndPrice(ticker)
    if data == -1:
        return None
    return data

async def getStocksFreeFloat(tickers):
    for ticker in tickers:
        ticker = __checkTicker(ticker)
    data = await __getStocksFloat(tickers)
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