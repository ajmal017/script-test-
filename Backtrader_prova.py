from backtrader import bt
from MACD_Strat import MACD_strat
import pandas as pd
from backtrader import CSVDataBase

cerebro = bt.Cerebro()
tick_data=pd.read_csv ('C:\\Users\\Riccardo\\PycharmProjects\\backtesting strategy\\AUDUSD-2020_01_01-2020_05_30.csv')
print(tick_data)
print('+++++++++')
tick_data[["time"]] = tick_data[["time"]].apply(pd.to_datetime)
tick_data.set_index("time", inplace=True)

tick_data_new = tick_data.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low'})
data=bt.feeds.PandasData(dataname=tick_data_new)
cerebro.adddata(data)

def ema(data, period=0, column='Close'):
    data['ema' + str(period)] = data[column].ewm(ignore_na=False, min_periods=period, com=period, adjust=True).mean()

    return data

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
print('-------')

cerebro.run()










# RUNNING BACKTEST BT
# bt = Backtest(tick_data_new, MACD_strat, cash=10000, commission=.002)
# bt.run()
# bt.plot()

# print(bt.run())

# funzione per ottimizzare
# bt.optimize(n1=range(5,100,5), n2=range(10,200,5), maximize='Equity Final [$]', constraint=lambda p: p.n1< p.n2)
