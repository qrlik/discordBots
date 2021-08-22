import asyncio
import bs4
import requests
import utils

__session = requests.Session() 
__session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' })
__url = 'https://www.sec.gov/'

def __getHtmlData():
    try:
        response = __session.get(__url + 'data/foiadocsfailsdatahtm')
        if response.ok:
            niceResponse = bs4.BeautifulSoup(response.text, features="lxml")
            responseTable = niceResponse.find('table', {'class': 'list'})
            if not responseTable:
                utils.log("ftd:__getHtmlData empty ftd table")
                return None
            ftdList = responseTable.find('tbody')
            if not ftdList:
                utils.log("ftd:__getHtmlData empty ftd list")
                return None
            return list(filter(lambda content: type(content) == bs4.Tag, ftdList.contents))
        else:
            utils.log('ftd:__getHtmlData not OK - reason ' + response.reason)
            return None
    except Exception as e:
        utils.log('ftd:__getHtmlData request error: ' + str(e))
    return -1

async def __getData():
    data = __getHtmlData()
    while not data:
        await asyncio.sleep(10)
        data = __getHtmlData()
    if data == -1:
        return None
    return data

async def parseFtd():
    data = await __getData();

if __name__ == '__main__':
    try:
        asyncio.run(parseFtd())
    except Exception as e:
        utils.log('main: error: ' + str(e))
