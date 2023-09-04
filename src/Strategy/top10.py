import backtrader as bt
import datetime
import datetime as dt
import sys
sys.path.append('../')
from Sizer.AvgStock import AvgStockSizer
buy_time = dt.datetime(2023, 8, 1, 13, 00, 00)
sell_time = dt.datetime(2023, 8, 1, 13, 44, 00)

class Top10Strategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('printlog', True),
    )


    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.datetime(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self, target):
        self.target = target
        self.dataopen = dict()
        self.dataclose = dict()
        self.order = dict()
        self.buyprice = dict()
        self.buycomm = dict()
        self.sma = dict()
        self.sizer = AvgStockSizer()
        # print(self.target[str(datetime.datetime(2022, 1, 8))])

        for data in self.datas:

            self.dataclose[data._name] = data.close
            self.dataopen[data._name] = data.open
            self.order[data._name] = None
            self.buyprice[data._name] = None
            self.buycomm[data._name] = None
            # self.sma[data._name] = bt.indicators.SimpleMovingAverage(
            #     data, period=self.params.maperiod)
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Order_id: %d, Stock: %s, Price: %.2f, Size %d, Comm %.2f' %
                     (order.ref,
                      order.data._name,
                      order.executed.price,
                      order.executed.size,
                      order.executed.comm))

                self.buyprice[order.data._name] = order.executed.price
                self.buycomm[order.data._name] = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Order_id: %d, Stock: %s, Price: %.2f, Size %d, Comm %.2f' %
                     (order.ref,
                      order.data._name,
                      order.executed.price,
                      order.executed.size,
                      order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            return

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    # def prenext(self):
    #     print("hi")
    #     self.datas[0].data.fillna(value=0, inplace=True)

    def next(self):
        cur_time = self.datetime.datetime()
        self.sizer.p.res_stock = 3
        # print(cur_time)
        for data in self.datas:
            print(cur_time)
            self.log('open: %.2f, close: %.2f' % (self.dataopen[data._name][0], self.dataclose[data._name][0]))
            if self.getposition(data).size == 0:
                if cur_time == buy_time:
                    # self.log('open: %.2f, close: %.2f' % (self.dataopen[data._name][0], self.dataclose[data._name][0]))
                    self.log('BUY CREATE, Stock: %s, Price: %.2f' % (data._name, self.dataopen[data._name][0]))
                    self.order[data._name] = self.buy(data=data, exectype=bt.Order.Limit,price=self.dataopen[data._name][0])
            if self.getposition(data).size != 0:
                if cur_time == sell_time:
                    self.log('SELL CREATE, Stock: %s, Price: %.2f' % (data._name, self.dataclose[data._name][0]))
                    # self.order[data._name] = self.sell(data=data, exectype=bt.Order.Limit,price=self.dataclose[data._name][0])
                    self.order[data._name] = self.close(data=data)


    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)
        return
