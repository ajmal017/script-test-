# importing tick data using duka
from backtesting import Backtest
from sma_crossover import SmaCross
from MACD_Strat import MACD_strat


##duka to download data
import duka.app.app as import_ticks_method
from duka.core.utils import TimeFrame
import datetime
import pandas as pd
# elements to import data from duka
import matplotlib.pyplot as plt
def ema(data, period=0, column='Close'):
    data['ema' + str(period)] = data[column].ewm(ignore_na=False, min_periods=period, com=period, adjust=True).mean()

    return data

# start_date =  datetime.date (2020,2,1)
# end_date =  datetime.date (2020,3,1)
# Assets = ["AUDUSD"]
# import_ticks_method (Assets, start_date, end_date, 1, TimeFrame.H1, ".", True)
tick_data = pd.read_csv("AUDUSD-2020_02_01-2020_03_01.csv")
tick_data[["time"]] = tick_data[["time"]].apply(pd.to_datetime)
tick_data.set_index("time", inplace=True)
print(tick_data)
print('++++++')
tick_data_new = tick_data.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low'})

print('-------')

remove_cols = []
if not 'ema' + str(26) in tick_data_new.columns:
    tick_data_new = ema(tick_data_new, 26)
    remove_cols.append('ema' + str(26))

if not 'ema' + str(12) in tick_data_new.columns:
    tick_data_new = ema(tick_data_new, 12)
    remove_cols.append('ema' + str(12))

tick_data_new['macd_val'] = tick_data_new['ema' + str(12)] - tick_data_new['ema' + str(26)]
tick_data_new['macd_signal_line'] = tick_data_new['macd_val'].ewm(ignore_na=False, min_periods=0, com=9,
                                                adjust=True).mean()
print(tick_data_new)
# RUNNING BACKTEST BT
bt = Backtest(tick_data_new, MACD_strat, cash=10000, commission=.002)
bt.run()
bt.plot()
print(bt.run())

# funzione per ottimizzare
# bt.optimize(n1=range(5,100,5), n2=range(10,200,5), maximize='Equity Final [$]', constraint=lambda p: p.n1< p.n2)
