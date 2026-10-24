# coding: utf-8
from applications.extensions import db


class AppAccessLog(db.Model):
    __tablename__ = 'app_access_log'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.BigInteger, nullable=False, index=True,  comment='uid')
    referer_url = db.Column(db.String(255), nullable=False,  comment='当前访问的refer')
    target_url = db.Column(db.String(255), nullable=False,  comment='访问的url')
    query_params = db.Column(db.Text, nullable=False, comment='get和post参数')
    ua = db.Column(db.String(255), nullable=False,  comment='访问ua')
    ip = db.Column(db.String(32), nullable=False,  comment='访问ip')
    note = db.Column(db.String(1000), nullable=False,  comment='json格式备注字段')
    created_time = db.Column(db.DateTime, nullable=False)
