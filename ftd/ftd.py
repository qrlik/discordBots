import asyncio
import bs4
import io
import re
import requests
import utils
import yahoo
import zipfile

__session = requests.Session() 
__session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' })
__url = 'https://www.sec.gov/'

class ftdInfo:
    url = ''
    date = ''
    data = {}

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
        return []
    return data

def __parseFtdInfo(tag):
    mainTag = None
    for content in tag.contents:
        if type(content) == bs4.Tag:
            mainTag = content
            break
    result = ftdInfo()
    for content in mainTag.contents:
        if type(content) == bs4.Tag:
            findResult = content.attrs.get('href')
            if findResult:
                result.url = __url + findResult
                result.date = content.text
                break
    if not result.url or not result.date:
        utils.log('ftd:__parseFtdInfo fail to parse ftdInfo')
        return None
    return result

def __getFile(url):
    try:
        response = __session.get(url)
        if response.ok:
            data = zipfile.ZipFile(io.BytesIO(response.content))
            list = data.namelist()
            if len(list) == 0:
                utils.log('ftd:__getFile empty archive')
                return -1
            with data.open(list[0]) as datafile:
                return datafile.read().decode("utf-8") 
        else:
            utils.log('ftd:__getFile not OK - reason ' + response.reason)
            return None
    except Exception as e:
        utils.log('ftd:__getFile request error: ' + str(e))
    return -1

async def __getFileData(url):
    data = __getFile(url)
    while not data:
        await asyncio.sleep(10)
        data = __getFile()
    if data == -1:
        return []
    return data

async def __sortFtdData(data):
    rows = data.split('\n')
    maxFtds = {}
    for row in rows:
        splitedRow = row.split('|')
        notDigitSearch = re.search(r'\D', splitedRow[0])
        if not notDigitSearch and splitedRow[0]:
            if maxFtds.setdefault(splitedRow[2], int(splitedRow[3])) < int(splitedRow[3]):
                maxFtds[splitedRow[2]] = int(splitedRow[3])

    splitedFtds = utils.splitDict(maxFtds, 250)

    tasks  = []
    for ftds in splitedFtds:
        tasks.append(asyncio.create_task(yahoo.getStocksFreeFloat(ftds)))
        
    floats = {}
    for task in tasks:
        freeFloatDict = await task
        floats.update(freeFloatDict)
        
    result = []
    for ticker, freeFloat in floats.items():
        div = float(maxFtds[ticker]) / freeFloat
        div100 = div * 100.0
        r = round(div100, 2)
        result.append((ticker, round(float(maxFtds[ticker]) / freeFloat * 100.0, 2)))
    result.sort(key=lambda tup: tup[1], reverse=True)
    return result

async def parseFtd():
    data = await __getData()
    for tag in data:
        ftd = __parseFtdInfo(tag)
        if ftd:
            dataStr = await __getFileData(ftd.url)
            if dataStr:
                ftd.data = await __sortFtdData(dataStr)
                with open(ftd.date + '.txt', 'x') as f:
                    for tupl in ftd.data:
                        f.write(tupl[0] + '\t\t' + str(tupl[1]) + '\n')


if __name__ == '__main__':
    try:
        asyncio.run(parseFtd())
    except Exception as e:
        utils.log('main: error: ' + str(e))
