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
    lastPostedId = 0

    def __init__(self):
        super().__init__()
        data = utils.loadJsonFile(self.__cacheFileName)
        self.lastPostedId = int(data.get('lastPostedId', 0))
        self.loop.create_task(self.dividendsTask())

    def saveCache(self):
        utils.saveJsonFile(self.__cacheFileName, {'lastPostedId': self.lastPostedId})

    async def on_ready(self):
        utils.log(f'{self.user} is connected', self)
        guild = discord.utils.find(lambda g: g.name == 'Ivanvest', self.guilds)
        self.__channel = discord.utils.find(lambda c: c.name == 'dividends', guild.channels)

    async def on_error(self, event):
        utils.log(event, self)

    async def dividendsTask(self):
        await self.wait_until_ready()

        #parse div
        #send messages
        #sleep 5 min

    def run(self):
        super().run(self.__token)




def main():
    bot = dividendsBot()
    bot.run()

    #divStocks = seekingAlpha.parseDivs()
    #ti = tinkoff.tinkoff()
    #stocks = []
    #for divInfo in divStocks:
    #    if divInfo.id == bot.lastPostedId:
    #        break

    #    stock = stockInfo.stockInfo(divInfo)

    #    if ti.getStock(stock.ticker):
    #        stock.isTinkoff = True
    #    stockNameAndPrice = yahoo.getStockNameAndPrice(stock.ticker)
    #    if not stockNameAndPrice:
    #        continue
    #    stock.name = stockNameAndPrice[0]
    #    stock.price = stockNameAndPrice[1]
    #    stock.div.divPercents = round(stock.div.amount / stock.price * 100, 2);
    #    stocks.append(stock)

    ##post messages in discord

    #bot.saveCache()


if __name__ == '__main__':
    main()