# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/25 17:23

@mark    : 布林通道策略
"""
import datetime
import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib
import akshare as ak



class Boll_strategy(bt.Strategy):
    # 自定义参数，每次买入1800手
    params = (('size', 1800),)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        ##使用自带的indicators中自带的函数计算出支撑线和压力线，period设置周期，默认是20
        self.lines.top = bt.indicators.BollingerBands(self.datas[0], period=20).top
        self.lines.bot = bt.indicators.BollingerBands(self.datas[0], period=20).bot

    def next(self):
        if not self.position:
            if self.dataclose <= self.lines.bot[0]:
                # 执行买入
                self.order = self.buy(size=self.params.size)
            else:
                if self.dataclose >= self.lines.top[0]:
                    # 执行卖出
                    self.order = self.sell(size=self.params.size)


# 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
stock_hfq_df = ak.stock_zh_a_hist(symbol="600309", adjust="hfq").iloc[:, :6]
# 处理字段命名，以符合 Backtrader 的要求
stock_hfq_df.columns = [
    'date',
    'open',
    'close',
    'high',
    'low',
    'volume',
]
# 把 date 作为日期索引，以符合 Backtrader 的要求
stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
start_date = datetime(1991, 4, 3)  # 回测开始时间
end_date = datetime(2022, 6, 16)  # 回测结束时间
data = bt.feeds.PandasData(dataname=stock_hfq_df,
                           fromdate=start_date,
                           todate=end_date)  # 加载数据
# 初始化cerebro回测系统设置
cerebro = bt.Cerebro()
# 将数据传入回测系统
cerebro.adddata(data)
# 将交易策略加载到回测系统中
cerebro.addstrategy(Boll_strategy)
# 设置初始资本为10,000
startcash = 1000000
cerebro.broker.setcash(startcash)
# 设置交易手续费为 0.25%
cerebro.broker.setcommission(commission=0.001)
# 运行回测系统
cerebro.run()
# 获取回测结束后的总资金
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash
# 打印结果
print(f'总资金: {round(portvalue, 2)}')
# 最后可视化
cerebro.plot()