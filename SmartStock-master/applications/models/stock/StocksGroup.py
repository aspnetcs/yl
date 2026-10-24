# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/5 10:46

@mark    :
"""
import datetime
from applications.extensions import db


class StocksGroup(db.Model):
    """
    分组管理
    """
    __tablename__ = 'stocks_group'

    id = db.Column(db.Integer, primary_key=True, comment='ID')
    name = db.Column(db.String(100), comment='分组名称')
    description = db.Column(db.String(200), comment='描述')
    user_id = db.Column(db.Integer, nullable=False, comment='创建者')
    flag = db.Column(db.Integer, default=0, comment='状态：0 not available, 1 available')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='更新时间')
    parent_id = db.Column(db.Integer, comment='父级id')
    is_top = db.Column(db.Integer, default=0, comment='是否置顶')
    stocks_type = db.Column(db.Integer, nullable=False, comment='项目类型：0根目录、1股票、2基金')

    def __init__(self, name, description, user_id, flag, create_time, update_time, parent_id, is_top, stocks_type):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.flag = flag
        self.create_time = create_time
        self.update_time = update_time
        self.parent_id = parent_id
        self.is_top = is_top
        self.stocks_type = stocks_type

    def __repr__(self):
        return '<StocksGroup id %r>' % self.id
