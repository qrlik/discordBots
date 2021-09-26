import asyncio
import discord
import tinkoff
import yahoo
import seekingAlpha
from dividends import stockInfo
import utils
import os

class discordBot(discord.Client):
    __token = os.getenv('DISCORD_TOKEN')
    __cacheFileName = 'botCache'
    __cache = []
    __config = {}
    __channel = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__config = utils.loadJsonFile('config')
        data = utils.loadJsonFile(self.__cacheFileName)
        if data:
            self.__cache = data

    async def __parseDivs(self):
        stocks = []
        divStocks = seekingAlpha.parseDivs()
        for divInfo in divStocks:
            if self.__isPosted(divInfo):
                continue

            stock = stockInfo.stockInfo(divInfo)
            stockNameAndPrice = await yahoo.getStockNameAndPrice(stock.ticker)
            if not stockNameAndPrice:
                continue
            if await tinkoff.getStock(stock.ticker):
                stock.isTinkoff = True
            stock.name = stockNameAndPrice[0]
            stock.price = round(stockNameAndPrice[1], 2)
            stock.div.percents = round(stock.div.amount / stock.price * 100, 2)
            stocks.append(stock)
        return stocks

    def __isPosted(self, divInfo):
        for posted in self.__cache:
            if [divInfo.ticker, divInfo.amount] == posted:
                return True
        return False

    def __saveToCache(self, stock):
        self.__cache.append((stock.ticker, stock.div.amount))
        if len(self.__cache) > self.__config['cacheSize']:
            self.__cache.pop(0)
        utils.saveJsonFile(self.__cacheFileName, self.__cache)

    async def __dividendsTask(self):
        while True:
            stocks = await self.__parseDivs()
            for stock in reversed(stocks):
                if not stock.isNeedToPost():
                    continue
                await self.__channel.send(embed=discord.Embed(colour=self.__config['embedColor'], description=str(stock)))
                self.__saveToCache(stock)
            await asyncio.sleep(self.__config['loopTimeout'])

    async def on_ready(self):
        utils.log(f'{self.user} is connected', self)
        guild = discord.utils.find(
            lambda g: g.id == self.__config['server'], self.guilds)
        self.__channel = discord.utils.find(
            lambda c: c.id == self.__config['channel'], guild.channels)
        self.loop.create_task(self.__dividendsTask())

    async def on_error(self, event):
        self.__saveCache()
        utils.log(event, self)

    def run(self):
        super().run(self.__token)


def main():
    bot = discordBot(allowed_mentions=discord.AllowedMentions(everyone=True))
    bot.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        utils.log('main: error: ' + str(e))
