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
        return self.name + '\t\t\t(' + self.ticker + ')\t' + str(self.isTinkoff) + '\t' + str(self.price) + '\t' + str(self.div.divPercents)

    div = divInfo.divInfo()
    ticker = ''
    name = ''
    price = 0
    isTinkoff = False
    
    
