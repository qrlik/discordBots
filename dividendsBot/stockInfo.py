import divInfo

class stockInfo:
    def __init__(self, divInfo):
        self.ticker = divInfo.ticker
        self.div = divInfo
    def __eq__(self, other):
        return self.div == other.div
    def __hash__(self):
        return hash(self.div)
    def __str__(self):
        result = self.name + ' (' + self.ticker + ') ' + str(self.price) + '$'
        if self.isTinkoff:
            result += ' - **Tinkoff**' 
        result += '\n' + str(self.div)
        return result

    def isMention(self):
        return self.isTinkoff and self.div.percents >= 2.0

    div = divInfo.divInfo()
    ticker = ''
    name = ''
    price = 0
    isTinkoff = False
    
    
