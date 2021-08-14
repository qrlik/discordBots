import requests
import re
import time
from bs4 import BeautifulSoup

class divInfo:
    def __eq__(self, other):
        return other and self.ticker == other.ticker and self.amount == other.amount
    def __hash__(self):
        return hash((self.ticker, self.amount))
    text = ''
    ticker = ''
    amount = 0.0
    id = 0
    
def _requestDivsTags():
    session = requests.Session() 
    session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' })
    url = 'https://seekingalpha.com/dividends/dividend-news'

    response = session.get(url).text
    niceResponse = BeautifulSoup(response, features="lxml")
    divList = niceResponse.find('ul', {'class': 'mc-list'})
    if not divList:
        return None
    return divList.find_all('li', {'class': 'mc'})

def _getDivsTags():
    divsTags = _requestDivsTags()
    while not divsTags:
        sleep(5)
        divsTags = _requestDivsTags()
    return divsTags

def _parseDiv(tagStrings):
    div = divInfo()
    divFlagFounded = False
    for string in tagStrings:
        searchDeclare = re.search(r'had\s+declare[s\s]', string)
        if searchDeclare:
            break

        searchTicket = re.search(r'[A-Z]+\.?[A-Z]+$', string)
        if searchTicket:
            div.ticker = searchTicket.group(0)
            continue
            
        searchDeclare = re.search(r'declare[s\s]', string)
        if searchDeclare:
            divFlagFounded = True
            continue

        if div.ticker and divFlagFounded:
            searchAmount = re.search(r'\d+\.\d+', string)
            if searchAmount:
                div.amount = float(searchAmount.group(0))
                break

    if not divFlagFounded or not div.ticker or not div.amount:
        return None
    return div

if __name__ == '__main__':
    divsList = []
    divsSet = set()

    divItems = _getDivsTags()
    for item in divItems:
        id = item.attrs.get('id', '')
        idSearch = re.search(r'\d{6,}$', id)
        if not id:
            continue
        id = idSearch.group(0)

        mediaBody = item.find('div', {'class': 'media-body'})
        if not mediaBody:
            continue

        divBody = mediaBody.find('div', {'class': 'bullets item-summary hidden'}).find('ul')
        firstBody = divBody.find('li')
        text = divBody.text

        div = _parseDiv(firstBody.strings)
        if not div:
            continue
        div.id = id

        if div in divsSet:
            continue
        div.text = text
        divsSet.add(div)
        divsList.append(div)

    for div in divsList:
        print(div.ticker + '\t' + str(div.amount) + '\t' + div.id + '\t' + div.text)
