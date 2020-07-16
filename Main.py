import backtrader as bt
import pandas as pd
from Main_Strategy import StrategiaProva
from backtrader.analyzers import (SQN, AnnualReturn, TimeReturn, SharpeRatio, TradeAnalyzer, DrawDown)


cerebro=bt.Cerebro()
cerebro.broker.setcash(10000)

data_raw=pd.read_csv ('C:\\Users\\Riccardo\\PycharmProjects\\backtesting strategy\\AUDUSD-2010_01_01-2020_05_30.csv')
data_raw[["time"]] = data_raw[["time"]].apply(pd.to_datetime)
data_raw.set_index("time", inplace=True)
data_raw_new = data_raw.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low'})
data=bt.feeds.PandasData(dataname=data_raw_new)

cerebro.adddata(data) #adding data to cerebro
cerebro.addstrategy(StrategiaProva) #adding strategy to cerebro


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.addsizer(bt.sizers.SizerFix, stake=10000) #sizer
cerebro.addobserver(bt.observers.DrawDown)

cerebro.run()

cerebro.plot(volume=False,style='candle',barup='green',bardown='red',timeframe=bt.TimeFrame.Minutes)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())








