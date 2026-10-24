# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/1/6 15:53

@mark    :
"""
import datetime
from applications.extensions import db


class StocksStrategy(db.Model):
    __tablename__ = 'stocks_strategy'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    name = db.Column(db.String(20), nullable=False, comment='策略名称')
    remarks = db.Column(db.Text(16777216), nullable=False, comment='备注')
    user_id = db.Column(db.Integer, comment='用户id')
    status = db.Column(db.Integer, default=0, comment='启用状态：0,1')
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='更新时间')
    type = db.Column(db.Integer, default=0, comment='策略类型：0个股,1单笔交易')
