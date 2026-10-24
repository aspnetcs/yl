# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/12/25 11:14 

@mark    :
"""
from applications.extensions import db


class StocksIndustryFundFlow(db.Model):
    """
    股票行业资金流向数据
    """
    __tablename__ = 'stocks_industry_fund_flow'
    __table_args__ = (
        db.Index('idx_industry_fund_flow_unique', 'code', 'report_date'),  # 添加复合索引
    )

    code = db.Column(db.String(20), primary_key=True, nullable=False, comment='行业代码')
    name = db.Column(db.String(50), comment='行业名称')
    zxj = db.Column(db.Float, comment='最新价')
    zdf = db.Column(db.Float, comment='涨跌幅')
    zsz = db.Column(db.Float, comment='总市值')
    hsl = db.Column(db.Float, comment='换手率')
    report_date = db.Column(db.DateTime, primary_key=True, nullable=False, comment='报告时间')
    update_time = db.Column(db.DateTime, nullable=False, comment='更新时间')
