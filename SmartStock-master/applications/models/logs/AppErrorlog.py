# coding: utf-8
from applications.extensions import db


class AppErrorLog(db.Model):
    __tablename__ = 'app_error_log'

    id = db.Column(db.Integer, primary_key=True)
    referer_url = db.Column(db.String(255), nullable=False,  comment='当前访问的refer')
    target_url = db.Column(db.String(255), nullable=False,  comment='访问的url')
    query_params = db.Column(db.Text, nullable=False, comment='get和post参数')
    content = db.Column(db.Text, nullable=False, comment='日志内容')
    created_time = db.Column(db.DateTime, nullable=False,  comment='插入时间')

