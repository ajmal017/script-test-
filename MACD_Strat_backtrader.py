'''
strategia da modificare
'''

from backtesting import Strategy
from backtesting.test import SMA
import pandas as pd
import backtrader



def ema(data, period=0, column='Close'):
    data['ema' + str(period)] = data[column].ewm(ignore_na=False, min_periods=period, com=period, adjust=True).mean()

    return data


class MACD_strat(Strategy):
    n1 = 200
    period_long = 26
    period_short = 12
    period_smoothing = 9
    sma1 = 0
    dataframe = pd.DataFrame()
    nextCount = 0
    Signal=0


    # DEFINING MACD INDICATOR
    def macd(data, period_long, period_short, period_smoothing):
        remove_cols = []
        if not 'ema' + str(period_long) in data.columns:
            data = ema(data, period_long)
            remove_cols.append('ema' + str(period_long))

        if not 'ema' + str(period_short) in data.columns:
            data = ema(data, period_short)
            remove_cols.append('ema' + str(period_short))

        data['macd_val'] = data['ema' + str(period_short)] - data['ema' + str(period_long)]
        data['macd_signal_line'] = data['macd_val'].ewm(ignore_na=False, min_periods=0, com=period_smoothing,
                                                        adjust=True).mean()

    # data = data.drop(remove_cols, axis=1)

class MyStrategy(bt.strategy):

    def init(self):
        # Precompute moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        # self.macd(self.period_long, self.period_short, self.period_smoothing)
        self.dataframe = pd.DataFrame(self.data.Close)
        dataframe1 = pd.DataFrame(self.data.Low)
        self.dataframe['Low'] = dataframe1['Low']
        dataframe1 = pd.DataFrame(self.data.Open)
        self.dataframe['Open'] = dataframe1['Open']
        dataframe1 = pd.DataFrame(self.data.High)
        self.dataframe['High'] = dataframe1['High']
        remove_cols = []
        if not 'ema' + str(26) in self.dataframe.columns:
            self.dataframe = ema(self.dataframe, 26)
            remove_cols.append('ema' + str(26))

        if not 'ema' + str(12) in self.dataframe.columns:
            self.dataframe = ema(self.dataframe, 12)
            remove_cols.append('ema' + str(12))

        self.dataframe['macd_val'] = self.dataframe['ema' + str(12)] - self.dataframe['ema' + str(26)]
        self.dataframe['macd_signal_line'] = self.dataframe['macd_val'].ewm(ignore_na=False, min_periods=0, com=9,
                                                                            adjust=True).mean()

        print(self.dataframe)
        print('**********')



    def next(self):
        if self.nextCount < 100:
            self.nextCount = self.nextCount + 1
            return

        if  self.dataframe['Close'][self.nextCount] > self.sma1 and \
            self.dataframe['macd_val'][self.nextCount] > self.dataframe['macd_signal_line'][self.nextCount] and \
            self.dataframe['macd_val'][self.nextCount] < 0 and self.dataframe['macd_signal_line'][self.nextCount] < 0:

            Signal=self.dataframe['Close'][self.nextCount]

            self.buy(price = Signal,sl = Signal-0.0010,tp = Signal+0.0030)
            print('buy')

        if  self.dataframe['Close'][self.nextCount]< self.sma1 and\
            self.dataframe['macd_val'][self.nextCount]< self.dataframe['macd_signal_line'][self.nextCount] and \
            self.dataframe['macd_val'][self.nextCount] > 0 and self.dataframe['macd_signal_line'][self.nextCount] >0:

            Signal=self.dataframe['Close'][self.nextCount]
            self.sell(price= Signal,sl = Signal+0.010, tp = Signal-0.0030)

            print('sell')

        self.nextCount = self.nextCount + 1


