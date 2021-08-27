from dividends import divInfo
import requests
import re
import time
import bs4
import utils

from selenium import webdriver
import chromedriver_binary

__session = requests.Session() 
__session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
                           'Accept-Language': 'en-US',
                           'Referer': 'http://www.google.com/',
                           'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
__url = 'https://seekingalpha.com/dividends/dividend-news'

class tickerInfo:
    name = ''
    ticker = ''
    price = 0.0
    freeFloat = 0

def __requestDivsTags():
    try:
        response = __session.get(__url)
    except requests.exceptions.RequestException as e:
        utils.log("seekingAlpha:__requestDivsTags request error: " + str(e))
        return None

    niceResponse = bs4.BeautifulSoup(response.text, features="lxml")
    divList = niceResponse.find('ul', {'class': 'mc-list'})
    if not divList:
        utils.log("seekingAlpha:__requestDivsTags empty div list")
        return None
    return divList.find_all('li', {'class': 'mc'})

def __getDivsTags():
    divsTags = __requestDivsTags()
    while not divsTags:
        sleep(10)
        divsTags = __requestDivsTags()
    return divsTags

def __getIdAndBody(item):
    mediaBody = item.find('div', {'class': 'media-body'})
    if not mediaBody:
        return None

    id = mediaBody.find('span', {'class': 'item-date'}).text;
    idSearch = re.search(r'\d{1,2}:\d\d.*$', id)
    if not idSearch:
        return None
    id = idSearch.group(0)

    hiddenBody = mediaBody.find('div', {'class': 'bullets item-summary hidden'})
    if not hiddenBody:
        return None
    ulBody = hiddenBody.find('ul')
    if not ulBody:
        return None
    return (id, ulBody)

def __parseDiv(tag):
    text = tag.text
    if re.search(r'had\s+declare[s\s]', text):
        return None
    if re.search(r'not\s+declare[s\s]', text):
        return None
    if not re.search(r'declare[s\s]', text):
        return None

    div = divInfo.divInfo()
    for string in tag.strings:
        if not div.ticker:
            searchTicket = re.search(r'[A-Z]+(\.[A-Z]+)?$', string)
            if searchTicket:
                div.ticker = searchTicket.group(0)
            continue
            
        if div.amount == 0.0:
            searchAmount = re.search(r'\d+\.\d+', string)
            if searchAmount:
                div.amount = float(searchAmount.group(0))
            continue

        searchAmount = re.search(r'\d+\.\d+', string)
        if searchAmount:
            div.yearYield = float(searchAmount.group(0))
            continue

        splitStr = string.split(';')
        for str in splitStr:
            if not div.payable:
                payable = re.match(r'payable.*', str, re.IGNORECASE)
                if payable:
                    div.payable = payable.group(0).title()
                    continue
            if not div.record:
                record = re.search(r'record.*', str, re.IGNORECASE)
                if record:
                    div.record = record.group(0).title()
                    continue
            if not div.exDiv:
                exDiv = re.search(r'ex-div.*$', str, re.IGNORECASE)
                if exDiv:
                    div.exDiv = exDiv.group(0).title()
                    continue
        if div.payable or div.record or div.exDiv:
            break

    for element in tag.find('li'):
        if type(element) == bs4.Tag:
            if element.attrs.get('target', '') == '_blank':
                div.link = element.attrs.get('href', '')
                break

    if not div.ticker or not div.amount:
        return None
    return div

def parseDivs():
    divsList = []
    divsSet = set()
    divItems = __getDivsTags()
    for item in reversed(divItems):
        idAndBody = __getIdAndBody(item)
        if not idAndBody:
            continue

        div = __parseDiv(idAndBody[1])
        if not div:
            continue
        div.id = idAndBody[0]

        if div in divsSet:
            continue
        divsSet.add(div)
        divsList.insert(0, div)
    return divsList

def __getTickerInfo(ticker):
    driver = webdriver.Chrome()
    driver.get('https://seekingalpha.com/symbol/' + ticker + '/overview')

    try:
        response = __session.get('https://seekingalpha.com/symbol/' + ticker)
    except requests.exceptions.RequestException as e:
        utils.log("seekingAlpha:__getTickerInfo request error: " + str(e))
        return None
    
    niceResponse = bs4.BeautifulSoup(response.text, features="lxml")
    grid = niceResponse.find('div', {'class': 'root'})
    tabContent = niceResponse.find('div', {'class': '__8f906-2Zlb9 __8f906-39OyF __8f906-2Fp2j'})
    tabContent2 = niceResponse.find('div', {'class': '__8f906-1wxqY __8f906-Fx3Go' })
    outstanding = tabContent2.find('td', { 'id': 'shareStatsShareOutstandingCurrent' })
    for string in tabContent2.elements:
        test = ''

    if not divList:
        utils.log("seekingAlpha:__requestDivsTags empty div list")
        return None
    return divList.find_all('li', {'class': 'mc'})

if __name__ == '__main__':
    __getTickerInfo('PRRWF')