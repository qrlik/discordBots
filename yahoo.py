import json
import requests
from enum import Enum

__API_URL = 'https://query2.finance.yahoo.com/'
__SUMMARY = 'v10/finance/quoteSummary/'
__MODULES = '?modules='

__session = requests.Session() 
__session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' })

class eModule(Enum):
    FINANCIAL = 1

moduleDict = {eModule.FINANCIAL: 'financialData'}

def __getRequestUrl(ticker, module):
    return __API_URL + __SUMMARY + ticker + __MODULES + module

def __getStockPrice(ticker):
    try:
        url = __getRequestUrl(ticker, moduleDict[eModule.FINANCIAL])
        response = __session.get(url)
        if response.ok:
            return response.json()['quoteSummary']['result'][0]['financialData']['currentPrice']['raw']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Request error: ", e)
    return -1

def getStockPrice(ticker):
    price = __getStockPrice(ticker)
    while not price:
        sleep(10)
        price = __getStockPrice(ticker)
    return price








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