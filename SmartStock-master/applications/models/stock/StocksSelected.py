# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/1/6 15:53

@mark    :
"""
import datetime
from applications.extensions import db


class StocksSelected(db.Model):
    __tablename__ = 'stocks_selected'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    user_id = db.Column(db.Integer, comment='用户id')
    code = db.Column(db.String(20), nullable=False, comment='股票编码')
    name = db.Column(db.String(20), nullable=False, comment='股票名称')
    group_id = db.Column(db.Integer, nullable=False, comment='分组id')
    is_hold = db.Column(db.Integer, nullable=False, default=0, comment='是否持仓')
    stock_type = db.Column(db.Integer, nullable=False, comment='类型：1股票；2基金')
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='更新时间')
    cost_price = db.Column(db.Float, default=0, comment='成本价')
    hold_number = db.Column(db.Float, default=0, comment='持股数')
    is_news = db.Column(db.Integer, nullable=False, default=0, comment='是否抓取新闻')
    total_invest_budget = db.Column(db.Float, default=0, comment='总投入预算')
    income_rate_target = db.Column(db.Float, default=0, comment='目标收益率')
