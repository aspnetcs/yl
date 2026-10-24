# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/3/3 17:54

@mark    :
"""
from applications.extensions import db


class StocksYjkbReport(db.Model):
    __tablename__ = 'stocks_yjkb_report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    code = db.Column(db.String(20), comment='股票代码')
    name = db.Column(db.String(50), comment='股票名称')
    mgsy = db.Column(db.Float, comment='每股收益')
    yysr_yysr = db.Column(db.Float, comment='营业收入-营业收入')
    yysr_tbzz = db.Column(db.Float, comment='营业收入-同比增长')
    yysr_jdhbzz = db.Column(db.Float, comment='营业收入-季度环比增长')
    jlr_jlr = db.Column(db.Float, comment='净利润-净利润')
    jlr_tbzz = db.Column(db.Float, comment='净利润-同比增长')
    jlr_jdhbzz = db.Column(db.Float, comment='净利润-季度环比增长')
    mgjzc = db.Column(db.Float, comment='每股净资产')
    jzcsyl = db.Column(db.Float, comment='净资产收益率')
    mgjyxjll = db.Column(db.Float, comment='每股经营现金流量')
    xsmll = db.Column(db.Float, comment='销售毛利率')
    schy = db.Column(db.String(50), comment='所处行业')
    zxggrq = db.Column(db.String(50), comment='最新公告日期')
    report_date = db.Column(db.String(50), nullable=False, comment='报告日期')
    report_type = db.Column(db.String(50), nullable=False, comment='报告类型')
    update_time = db.Column(db.DateTime, nullable=False, comment='创建时间')
