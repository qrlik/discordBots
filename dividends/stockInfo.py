from dividends import divInfo

class stockInfo:
    def __init__(self, divInfo):
        self.ticker = divInfo.ticker
        self.div = divInfo
    def __eq__(self, other):
        return self.div == other.div
    def __hash__(self):
        return hash(self.div)
    def __str__(self):
        result = ''
        #if self.isTinkoff:
        #    result += '**```fix\nTinkoff```**' 
        result += self.name + ' (' + self.ticker + ') - ' + str(self.price) + '$'
        result += '\n' + str(self.div)
        return result

    def isNeedToPost(self):
        return self.isTinkoff and self.div.percents >= 1.0

    div = divInfo.divInfo()
    ticker = ''
    name = ''
    price = 0
    isTinkoff = False
    
    
