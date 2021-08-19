import asyncio
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
    __channel = None
    __lastPostedId = 0

    def __init__(self):
        super().__init__()
        data = utils.loadJsonFile(self.__cacheFileName)
        self.__lastPostedId = int(data.get('lastPostedId', 0))

    def __parseDivs(self):
        stocks = []
        divStocks = seekingAlpha.parseDivs()
        for divInfo in divStocks:
            if divInfo.id == self.__lastPostedId:
                break

            stock = stockInfo.stockInfo(divInfo)
            stockNameAndPrice = yahoo.getStockNameAndPrice(stock.ticker)
            if not stockNameAndPrice:
                continue
            if tinkoff.getStock(stock.ticker):
                stock.isTinkoff = True
            stock.name = stockNameAndPrice[0]
            stock.price = stockNameAndPrice[1]
            stock.div.percents = round(stock.div.amount / stock.price * 100, 2);
            stocks.append(stock)
        return stocks

    def __saveCache(self):
        utils.saveJsonFile(self.__cacheFileName, {'lastPostedId': self.__lastPostedId})
        
    async def __dividendsTask(self):
        while True:
            stocks = self.__parseDivs()
            for stock in reversed(stocks):
                await self.__channel.send('```' + str(stock) + '```')
                self.__lastPostedId = stock.div.id
                self.__saveCache()
            await asyncio.sleep(300)

    async def on_ready(self):
        utils.log(f'{self.user} is connected', self)
        guild = discord.utils.find(lambda g: g.name == 'Ivanvest', self.guilds)
        self.__channel = discord.utils.find(lambda c: c.name == 'dividends', guild.channels)
        self.loop.create_task(self.__dividendsTask())

    async def on_error(self, event):
        __saveCache()
        utils.log(event, self)

    def run(self):
        super().run(self.__token)

def main():
    bot = dividendsBot()
    bot.run()

if __name__ == '__main__':
    main()