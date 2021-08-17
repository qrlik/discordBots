import discord
import tinkoff
import yahoo
import seekingAlpha
import stockInfo
import utils
import os

class dividendsBot(discord.Client):
    __cacheFileName = 'dividendsBotCache'
    __token = os.getenv('DISCORD_TOKEN')
    lastPostedId = 0

    def __init__(self):
        super().__init__()
        data = utils.loadJsonFile(self.__cacheFileName)
        self.lastPostedId = int(data.get('lastPostedId', 0))
        super().run(self.__token)

    async def on_ready(self):
        utils.log(f'{self.user} is connected', self)

    async def on_error(self, event):
        utils.log(event, self)


def main():
    bot = dividendsBot()
    divStocks = seekingAlpha.parseDivs()
    ti = tinkoff.tinkoff()
    stocks = []
    for divInfo in divStocks:
        if divInfo.id == bot.lastPostedId:
            break

        stock = stockInfo.stockInfo(divInfo)

        if ti.getStock(stock.ticker):
            stock.isTinkoff = True
        stockNameAndPrice = yahoo.getStockNameAndPrice(stock.ticker)
        if not stockNameAndPrice:
            continue
        stock.name = stockNameAndPrice[0]
        stock.price = stockNameAndPrice[1]
        stock.div.divPercents = round(stock.div.amount / stock.price * 100, 2);
        stocks.append(stock)

    #post messages in discord

    utils.saveJsonFile(__cacheFileName, {'lastPostedId': bot.lastPostedId})


if __name__ == '__main__':
    main()