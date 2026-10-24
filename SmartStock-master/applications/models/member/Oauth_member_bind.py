# coding: utf-8
import datetime
from applications.extensions import db


class OauthMemberBind(db.Model):
    __tablename__ = 'oauth_member_bind'
    __table_args__ = (
        db.Index('idx_type_openid', 'type', 'openid'),
    )
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String(11), nullable=False,  comment='会员id')
    client_type = db.Column(db.String(20), comment='客户端来源类型。qq,weibo,weixin')
    type = db.Column(db.Integer,  comment='类型 type 1:wechat ')
    openid = db.Column(db.String(80),  comment='第三方id')
    unionid = db.Column(db.String(100), comment='unionid')
    extra = db.Column(db.Text, comment='额外字段')
    updated_time = db.Column(db.DateTime, nullable=False, default= str(datetime.datetime.now()),  comment='最后更新时间')
    created_time = db.Column(db.DateTime, nullable=False, default= str(datetime.datetime.now()),  comment='插入时间')
