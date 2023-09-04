import os
import pandas as pd
import re
import sys
import datetime as dt
from datetime import datetime

# import backtrader modules
sys.path.append('./backtrader')
import backtrader as bt

# import customized module
from DataLoader.YuanTaFormat import YuantaPandasData
from DataLoader.YuanTaFormat import CryptoPandasData
from DataLoader.YuanTaFormat import shioajiPandasData
from Strategy.top10 import Top10Strategy





if __name__ == '__main__':
  print("hello backtrader!")

  # Create a cerebro entity
  cerebro = bt.Cerebro(oldsync=False)

  buy_time = dt.datetime(2022, 1, 2, 7, 55, 00)
  sell_time = dt.datetime(2022, 1, 2, 23, 55, 00)


  # Load dataset from directories
  start_date = dt.datetime(2020, 7, 1)
  end_date = dt.datetime(2023, 8, 1)

  # trade_time = dt.datetime.combine(datetime.date(2011, 1, 1), datetime.time(10, 23))
  a = dt.datetime.combine(dt.date(2011, 1, 1), dt.time(10, 23))

  data_path = "../data/future_test2/"
  for file in os.listdir(data_path):
    stock_id = file.split(".")[0]
    print("Load ", stock_id)
    df = pd.read_csv(os.path.join(data_path, file))
    df = df.fillna(0)
    print(df)
    data = shioajiPandasData(dataname = df, fromdate = start_date, todate = end_date, nullvalue = 0)
    # data = shioajiPandasData(dataname=df)
    cerebro.adddata(data, name = stock_id)

    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=60, name = stock_id)
  #missing target: ['DUF', 'MCF']
  target_path = "../data/top_10/"
  target = {}
  all_target = set()
  for file in os.listdir(target_path):
    date = datetime.strptime(file.split(".")[0], "%Y_%m_%d")
    df = pd.read_csv(os.path.join(target_path, file))
    target[str(date)] = list(df["商品代號"])
    all_target.update(list(df["商品代號"]))


  # Add Strategy
  cerebro.addstrategy(Top10Strategy, target)

  # 当日下单，当日开盘价成交
  # cerebro.broker.set_coo(True)
  cerebro.broker.setcash(100000.0)
  cerebro.broker.setcommission(commission=0.001)
  # 设置买入设置，固定买卖数量
  # cerebro.addsizer(AvgStockSizer)
  cerebro.run()

  print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
  # cerebro.plot()











