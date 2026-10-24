# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/1/6 15:53

@mark    :
"""
import datetime
from applications.extensions import db


class StocksNews(db.Model):
    __tablename__ = 'stocks_news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    code = db.Column(db.String(20), nullable=False, comment='股票编码')
    name = db.Column(db.String(20), nullable=False, comment='股票名称')
    title = db.Column(db.String(500), nullable=False, comment='标题')
    contents = db.Column(db.Text(16777216), comment='内容')
    publish_time = db.Column(db.DateTime, comment='发布时间')
    act_source = db.Column(db.String(500), comment='文章来源')
    url = db.Column(db.Text(16777216), comment='url')
    is_hot = db.Column(db.Integer, nullable=False, default=0, comment='是否热点')
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='更新时间')
    positive_prob = db.Column(db.Float, nullable=False, default=0, comment='正面概率')
    negative_prob = db.Column(db.Float, nullable=False, default=0, comment='负面概率')
    sentiment = db.Column(db.String(20), nullable=False, comment='情感')

