import backtrader as bt
import math


class AvgStockSizer(bt.Sizer):
    params = (
        ('res_stock', 1),
    )

    def _getsizing(self, comminfo, cash, data, isbuy):
        size = cash / (self.p.res_stock*data.close)
        size = math.floor(size / 1) * 1
        return size