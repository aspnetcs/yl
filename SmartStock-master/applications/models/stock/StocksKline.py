# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 16:12

@mark    :
"""
from applications.extensions import db


class StocksKline(db.Model):
    """
    股票k线数据
    """
    __tablename__ = 'stocks_kline'
    __table_args__ = (
        db.Index('idx_kline_unique', 'region', 'code', 'report_time'),  # 添加复合索引
    )

    region = db.Column(db.String(20), primary_key=True, nullable=False, comment='市场代码：GB=指数，SH=上证，SZ=深证，HK=港股')
    code = db.Column(db.String(20), primary_key=True, nullable=False, comment='股票代码')
    name = db.Column(db.String(50), comment='股票名称')
    zxj = db.Column(db.Float, comment='最新价')
    cjl = db.Column(db.Float, comment='成交量')
    cje = db.Column(db.Float, comment='成交额')
    zg = db.Column(db.Float, comment='最高')
    zd = db.Column(db.Float, comment='最低')
    jk = db.Column(db.Float, comment='今开')
    report_time = db.Column(db.DateTime, primary_key=True, nullable=False, comment='报告时间')
    update_time = db.Column(db.DateTime, nullable=False, comment='更新时间')
