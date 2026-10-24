# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 16:12

@mark    :
"""
from applications.extensions import db


class StocksAnalyse(db.Model):
    __tablename__ = 'stocks_analyse'

    __table_args__ = (
        db.Index('idx_stocks_analyse_unique', 'region', 'code'),  # 添加复合索引
    )

    region = db.Column(db.String(20), primary_key=True, nullable=False,
                       comment='市场代码：GB=指数，SH=上证，SZ=深证，HK=港股')
    code = db.Column(db.String(20), primary_key=True, nullable=False, comment='股票代码')
    name = db.Column(db.String(50), comment='股票名称')
    zsz = db.Column(db.Float, comment='总市值')
    ltsz = db.Column(db.Float, comment='流通市值')
    syl_dt = db.Column(db.Float, comment='市盈率-动态')
    sjl = db.Column(db.Float, comment='市净率')
    zxj = db.Column(db.Float, comment='最新价')
    zdf_60d = db.Column(db.Float, comment='60日涨跌幅')
    zdf_nzj = db.Column(db.Float, comment='年初至今涨跌幅')

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
    report_date = db.Column(db.String(50), comment='报告日期')
    update_time = db.Column(db.DateTime, nullable=False, comment='创建时间')
