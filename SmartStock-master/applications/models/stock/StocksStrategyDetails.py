# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/1/6 15:53

@mark    :
"""
import datetime
from applications.extensions import db


class StocksStrategyDetails(db.Model):
    __tablename__ = 'stocks_strategy_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    user_id = db.Column(db.Integer, comment='用户id')
    code = db.Column(db.String(20), nullable=False, comment='股票编码')
    name = db.Column(db.String(20), nullable=False, comment='股票名称')
    zxj = db.Column(db.Float, default=0, comment='最新价')
    total_invest_budget = db.Column(db.Float, default=0, comment='总投入预算')
    total_invested = db.Column(db.Float, default=0, comment='总投入')
    zdf_stg = db.Column(db.Float, default=0, comment='涨跌幅策略')
    zde_stg = db.Column(db.Float, default=0, comment='涨跌额策略')
    next_price_buy = db.Column(db.Float, default=0, comment='下一买点')
    income_rate_target = db.Column(db.Float, default=0, comment='目标收益率')
    income_target = db.Column(db.Float, default=0, comment='目标收益')
    next_price_sell = db.Column(db.Float, default=0, comment='下一卖点')
    is_monitor = db.Column(db.Integer, nullable=False, default=0, comment='是否触发监控')
    strategy_id = db.Column(db.Integer, nullable=False, default=0, comment='策略ID')
    selected_id = db.Column(db.Integer, nullable=False, default=0, comment='自选股ID')
    suggest_buy_num = db.Column(db.Float, nullable=False, default=0, comment='建议买入股数')
    suggest_buy_amt = db.Column(db.Float, nullable=False, default=0, comment='建议买入金额')
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='更新时间')
    view_price = db.Column(db.Float, default=0, comment='观察价格')
    add_fund = db.Column(db.Float, default=0, comment='加仓幅度')

