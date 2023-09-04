import pandas as pd
from backtrader.feeds import PandasData


class YuantaPandasData(PandasData):
    params = (
        ('datetime', "日期"),
        ('open', "開盤"),
        ('high', "最高"),
        ('low', "最低"),
        ('close', "收盤"),
        ('volume', " 成交量"),
    )

    def __init__(self):
        self.p.dataname["日期"] =  pd.to_datetime(self.p.dataname["日期"])
        super().__init__()

class CryptoPandasData(PandasData):
    params = (
        ('datetime', "Datetime"),
        ('open', "Open"),
        ('high', "High"),
        ('low', "Low"),
        ('close', "Close"),
        ('volume', "TotalVolume"),
    )

    def __init__(self):
        self.p.dataname["Datetime"] =  pd.to_datetime(self.p.dataname["Datetime"])
        super().__init__()

class shioajiPandasData(PandasData):
    params = (
        ('nullvalue', float('NaN')),

        ('datetime', "ts"),
        ('open', "Open"),
        ('high', "High"),
        ('low', "Low"),
        ('close', "Close"),
        ('volume', "Volume"),
    )

    def __init__(self):
        self.p.dataname["ts"] =  pd.to_datetime(self.p.dataname["ts"])
        super().__init__()