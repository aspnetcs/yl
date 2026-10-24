# coding: utf-8
import datetime

from applications.extensions import db


class MemberUser(db.Model):
    __tablename__ = 'member_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    nickname = db.Column(db.String(100), comment='会员名')
    mobile = db.Column(db.String(11), comment='会员手机号码')
    sex = db.Column(db.Integer, comment='性别 0:未知 1：男 2：女')
    avatar = db.Column(db.String(200), comment='会员头像')
    salt = db.Column(db.String(32), comment='随机salt')
    reg_ip = db.Column(db.String(100), comment='注册的ip')
    status = db.Column(db.Integer, nullable=False, default=1, comment='状态 1：正常 0：无效')
    updated_time = db.Column(db.DateTime, nullable=False, default= str(datetime.datetime.now()), comment='最后一次更新时间')
    created_time = db.Column(db.DateTime, nullable=False, default= str(datetime.datetime.now()), comment='创建时间')

    role = db.relationship('MemberRole', secondary="member_user_role", backref=db.backref('user'), lazy='dynamic')
