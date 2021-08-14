import requests
import re
import time
from bs4 import BeautifulSoup

class divInfo:
    def __eq__(self, other):
        return other and self.ticker == other.ticker and self.amount == other.amount
    def __hash__(self):
        return hash((self.ticker, self.amount))

    ticker = ''
    payable = ''
    exDiv = ''
    record = ''
    amount = 0.0
    yearYield = 0.0
    id = 0
    
def _requestDivsTags():
    session = requests.Session() 
    session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' })
    url = 'https://seekingalpha.com/dividends/dividend-news'

    try:
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print("Request error: ", e)
        return None

    niceResponse = BeautifulSoup(response.text, features="lxml")
    divList = niceResponse.find('ul', {'class': 'mc-list'})
    if not divList:
        return None
    return divList.find_all('li', {'class': 'mc'})

def _getDivsTags():
    divsTags = _requestDivsTags()
    while not divsTags:
        sleep(10)
        divsTags = _requestDivsTags()
    return divsTags

def _getIdAndBody(item):
    id = item.attrs.get('id', '')
    idSearch = re.search(r'\d{6,}$', id)
    if not idSearch:
        return None
    id = idSearch.group(0)

    mediaBody = item.find('div', {'class': 'media-body'})
    if not mediaBody:
        return None
    hiddenBody = mediaBody.find('div', {'class': 'bullets item-summary hidden'})
    if not hiddenBody:
        return None
    ulBody = hiddenBody.find('ul')
    if not ulBody:
        return None
    return (id, ulBody)

def _parseDiv(text, strings):
    if re.search(r'had\s+declare[s\s]', text):
        return None
    if not re.search(r'declare[s\s]', text):
        return None

    div = divInfo()
    for string in strings:
        if not div.ticker:
            searchTicket = re.search(r'[A-Z]+\.?[A-Z]+$', string)
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

    if not div.ticker or not div.amount:
        return None
    return div

def parseDivs():
    divsList = []
    divsSet = set()
    divItems = _getDivsTags()
    for item in divItems:
        idAndBody = _getIdAndBody(item)
        if not idAndBody:
            continue

        div = _parseDiv(idAndBody[1].text, idAndBody[1].strings)
        if not div:
            continue
        div.id = idAndBody[0]

        if div in divsSet:
            continue
        divsSet.add(div)
        divsList.append(div)
    return divsList

if __name__ == '__main__':
    for div in parseDivs():
        print(div.ticker + '\t' + str(div.amount) + '\t' + div.id + '  \t' + str(div.yearYield) + '  \t' + div.exDiv + '  \t' + div.record + '   \t' + div.payable)
