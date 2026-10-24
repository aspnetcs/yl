# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/12/9 9:05 

@mark    :
'''
from applications.extensions import db


class MemberCollection(db.Model):
    __tablename__ = 'member_collection'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    member_id = db.Column(db.String(11), nullable=False, primary_key=True, comment='用户ID')
    power_id = db.Column(db.Integer, nullable=False, comment='报表ID')
    collect_type = db.Column(db.Integer, nullable=False, comment='类型：1：报表 0：首页')
    created_time = db.Column(db.DateTime, nullable=False, comment='最后一次更新时间')
