# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/3/7 17:16

@mark    :
"""
from applications.extensions import db


class StocksQuantify(db.Model):
    __tablename__ = 'stocks_quantify'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    user_id = db.Column(db.Integer, comment='用户id')
    name = db.Column(db.String(255), comment='名称')
    filter = db.Column(db.Text(16777216), comment='筛选条件json')
    mark = db.Column(db.Text(16777216), comment='备注')
    update_time = db.Column(db.DateTime, nullable=False, comment='创建时间')
