import json
import requests
import time
from enum import Enum

__API_URL = 'https://query2.finance.yahoo.com/'
__SUMMARY = 'v10/finance/quoteSummary/'
__MODULES = '?modules='

__session = requests.Session() 
__session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' })

class eModule(Enum):
    PRICE = 1
    FINANCIAL = 2

moduleDict = {eModule.PRICE: 'price',
              eModule.FINANCIAL: 'financialData'}

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
            name = price['longName'] if price['longName'] else price['shortName']
            return (name, price['regularMarketPrice']['raw'])
        else:
            print('yahoo:__getStockNameAndPrice ' + ticker + ' reason ' + response.reason)
            if 'Not Found' not in response.reason:
                return None
    except requests.exceptions.RequestException as e:
        print('yahoo:__getStockNameAndPrice request error: ', e)
    return ('ERROR', -1)

def getStockNameAndPrice(ticker):
    ticker = __checkTicker(ticker)
    data = __getStockNameAndPrice(ticker)
    while not data:
        time.sleep(10)
        data = __getStockNameAndPrice(ticker)
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