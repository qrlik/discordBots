
class divInfo:
    def __eq__(self, other):
        return other and self.ticker == other.ticker and self.amount == other.amount
    def __hash__(self):
        return hash((self.ticker, self.amount))
    def __str__(self):
        result = 'declared ' + str(self.amount) + '$ (' + str(self.percents) + '%) divs'
        if self.yearYield > 0.0:
            result += ' - Y/Y ' + str(self.yearYield) + '%'
        result += '\n' + self.exDiv + ' - ' + self.record + ' - ' + self.payable
        return result

    ticker = ''
    payable = ''
    exDiv = ''
    record = ''
    amount = 0.0
    yearYield = 0.0
    percents = 0.0
    id = ''

