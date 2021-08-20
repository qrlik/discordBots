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
    __lastPostedId = ''
    __lastPostedTicker = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = utils.loadJsonFile(self.__cacheFileName)
        if data:
            self.__lastPostedId = data.get('lastPostedId', '')
            self.__lastPostedTicker = data.get('lastPostedTicker', '')

    def __parseDivs(self):
        stocks = []
        divStocks = seekingAlpha.parseDivs()
        for divInfo in divStocks:
            if divInfo.id == self.__lastPostedId and divInfo.ticker == self.__lastPostedTicker:
                break

            stock = stockInfo.stockInfo(divInfo)
            stockNameAndPrice = yahoo.getStockNameAndPrice(stock.ticker)
            if not stockNameAndPrice:
                continue
            if tinkoff.getStock(stock.ticker):
                stock.isTinkoff = True
            stock.name = stockNameAndPrice[0]
            stock.price = round(stockNameAndPrice[1], 2)
            stock.div.percents = round(stock.div.amount / stock.price * 100, 2);
            stocks.append(stock)
        return stocks

    def __saveCache(self):
        utils.saveJsonFile(self.__cacheFileName, {'lastPostedId': self.__lastPostedId, 'lastPostedTicker': self.__lastPostedTicker})
        
    async def __dividendsTask(self):
        while True:
            stocks = self.__parseDivs()
            for stock in reversed(stocks):
                message = '@everyone\n' + str(stock) if stock.isMention() else str(stock)
                await self.__channel.send(embed = discord.Embed(colour = 1327910, description = message))
                self.__lastPostedId = stock.div.id
                self.__lastPostedTicker = stock.ticker
                self.__saveCache()
            await asyncio.sleep(150)

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
    bot = dividendsBot(allowed_mentions = discord.AllowedMentions(everyone = True))
    bot.run()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        utils.log('main: error: ' + str(e))