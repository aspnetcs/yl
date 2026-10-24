# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/18 15:27

@mark    :
"""
import datetime
from applications.extensions import db


class StocksTradingDetails(db.Model):
    __tablename__ = 'stocks_trading_details'

    id = db.Column(db.Integer, primary_key=True, comment='ID')
    user_id = db.Column(db.Integer, comment='用户id')
    selected_id = db.Column(db.Integer, nullable=False, default=0, comment='自选股ID')
    trade_time = db.Column(db.DateTime, nullable=False, comment='交易时间')
    trade_type = db.Column(db.String(255), comment='业务名称')
    code = db.Column(db.String(20), comment='股票代码')
    name = db.Column(db.String(50), comment='股票名称')
    cjsl = db.Column(db.Float, comment='成交数量')
    cjjg = db.Column(db.Float, comment='成交价格')
    jyje = db.Column(db.Float, comment='交易金额')
    strategy_id = db.Column(db.Integer, nullable=False, default=0, comment='策略ID')
    is_monitor = db.Column(db.Integer, nullable=False, default=0, comment='是否触发监控')
    zdf_tg = db.Column(db.Float, default=0, comment='涨跌幅目标')
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='更新时间')
    next_price_buy = db.Column(db.Float, default=0, comment='下次购买价格')
    next_price_sell = db.Column(db.Float, default=0, comment='下次卖出价格')
    zxj = db.Column(db.Float, default=0, comment='当前价格')
