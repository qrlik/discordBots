
class divInfo:
    def __eq__(self, other):
        return other and self.ticker == other.ticker and self.amount == other.amount
    def __hash__(self):
        return hash((self.ticker, self.amount))

    ticker = ''
    payable = ''
    exDiv = ''
    record = ''
    amount = 0.0
    yearYield = 0.0
    divPercents = 0.0
    id = 0
    
def decodeJsonToDivInfo(divDict):
    result = divInfo()
    result.ticker = divDict.get('ticker', '')
    result.amount = divDict.get('amount', 0.0)
    result.yearYield = divDict.get('yearYield', 0.0)
    result.payable = divDict.get('payable', '')
    result.record = divDict.get('record', '')
    result.exDiv = divDict.get('exDiv', '')
    result.id = int(divDict.get('id', 0))
    result.divPercents = divDict.get('divPercents', 0.0)
    return result

