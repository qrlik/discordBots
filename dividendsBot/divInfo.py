
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

