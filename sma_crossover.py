'''
strategia da modificare
'''

from backtesting import Strategy
from backtesting.lib import crossover

from backtesting.test import SMA


#class SMA_Crossover(Strategy):
#    def init(self):
#        Close = self.data.Close
#        self.ma1 = self.I(SMA, Close, 50)
#         self.ma2 = self.I(SMA, Close, 100)

#     def next(self):
#         if crossover(self.ma1, self.ma2):
#             self.buy()
#         elif crossover(self.ma2, self.ma1):
#             self.sell()

class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 50
    n2 = 100

    def init(self):
        # Precompute two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        # If sma1 crosses above sma2, buy the asset
        if crossover(self.sma1, self.sma2):
            self.buy()

        # Else, if sma1 crosses below sma2, sell it
        elif crossover(self.sma2, self.sma1):
            self.sell()



