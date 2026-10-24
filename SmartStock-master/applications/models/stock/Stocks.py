# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 16:12

@mark    :
"""
from applications.extensions import db


class Stocks(db.Model):
    __tablename__ = 'stocks'

    region = db.Column(db.String(20), primary_key=True, nullable=False, comment='市场代码：GB=指数，SH=上证，SZ=深证，HK=港股')
    code = db.Column(db.String(20), primary_key=True, comment='股票代码')
    name = db.Column(db.String(50), comment='股票名称')
    zxj = db.Column(db.Float, comment='最新价')
    zdf = db.Column(db.Float, comment='涨跌幅')
    zde = db.Column(db.Float, comment='涨跌额')
    cjl = db.Column(db.Float, comment='成交量')
    cje = db.Column(db.Float, comment='成交额')
    syl_dt = db.Column(db.Float, comment='市盈率-动态')
    sjl = db.Column(db.Float, comment='市净率')
    zsz = db.Column(db.Float, comment='总市值')
    ltsz = db.Column(db.Float, comment='流通市值')
    zdf_60d = db.Column(db.Float, comment='60日涨跌幅')
    zdf_nzj = db.Column(db.Float, comment='年初至今涨跌幅')
    update_time = db.Column(db.DateTime, nullable=False, comment='更新时间')
