import backtrader as bt
from datetime import datetime

class StrategiaProva(bt.Strategy):
    MAparams=(('period',200),)
    params= (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('smaperiod', 200),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )


    def __init__(self):
        print('print init')

        #sma1 = bt.indicators.SMA(period=self.p.period)
        self.macd = bt.indicators.MACD(self.data, period_me1=self.p.macd1, period_me2=self.p.macd2, period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)


        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)


    def start(self):
        self.count = 0
        self.wasLong=False
        self.order = None  # sentinel to avoid operrations on pending order

    def notify_order(self, order):
        if order.status == order.Completed:
            print ('completato ',order.ref,": ",order.info, " index temporale da prec. ",self.count)
            print("================================")
            self.count=0
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def next(self):
        # 3 righe per stampare data e ora.
        dt = self.datas[0].datetime.date(0)
        currentTime = dt.strftime("%d/%m/%Y")
        time ='- '+currentTime + ' ' + str(self.data.datetime.time())+' -'
        pdist = 0.0010
        self.count = self.count + 1

        if self.order:
            print('return')
            return  # pending order execution

        if not self.position:  # not in the market
            if self.mcross[0] > 0.0 and self.data.close[0]>self.sma and self.macd.macd < 0 and self.macd.signal < 0: #conditions for long
                print("- I'm NOT in the market")
                self.pstop = self.data.close[0] - pdist
                self.order=self.buy()
                self.order.addinfo(name='Long Market Entry')
                self.wasLong=True
                self.ptarget=self.data.close[0]+(pdist*3)
                print( '%s' % time,'buy;','price=', self.data.close[0],'stop=',self.pstop, 'target=',self.ptarget)

            elif self.mcross[0] < 0.0 and self.data.close[0]<self.sma and self.macd.macd > 0 and self.macd.signal > 0: #conditions for short
                print("- I'm NOT in the market")
                self.pstop = self.data.close[0] + pdist
                self.order = self.sell()
                self.order.addinfo(name='Short Market Entry')
                self.wasLong = False
                self.ptarget = self.data.close[0] - (pdist * 3)
                print('%s' % time,'sell;','price=',self.data.close[0],'stop=',self.pstop,'target=', self.ptarget)

        else:  # in the market
            if self.wasLong: #if position long
                print("\n$ If position long time: ",time,"\n")
                ptarget = self.ptarget
                if self.data.high[0]>ptarget :
                    print("+ I'm in the market")
                    self.order =self.close() #exit position target reach
                    self.order.addinfo(name='Close Buy Target')
                    print('*** details: ',time,self.data.high[0], ptarget)
                elif self.data.low[0]<self.pstop:
                    print("+ I'm in the market")
                    self.order =self.close() #exit position stopped out
                    self.order.addinfo(name='Close Buy Stopped')
                    print('*** details: ',time, self.data.low[0], self.pstop)

            elif not self.wasLong: #if position is short
                print("\n$ If position short time: ", time, "\n")
                ptarget = self.ptarget
                if self.data.low[0]<ptarget:
                    print("+ I'm in the market")
                    self.order =self.close() #exit position target reach
                    self.order.addinfo(name='Close Sell Target')
                    print('*** details: ',time, ptarget)
                elif self.data.high[0]>self.pstop:
                    print("+ I'm in the market")
                    self.order =self.close() #exit position stopped out
                    self.order.addinfo(name='Close Sell Stopped')
                    print ('*** details: ', time, self.pstop)
