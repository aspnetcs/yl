# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/7/29 20:48

@mark    :
"""
from applications.extensions import db


class StockMsgQueue(db.Model):
    __tablename__ = 'stock_msg_queue'
    __table_args__ = (
        db.Index('idx_msg_unique', 'strategy_details_id', 'strategy_type',
                 'code', 'msg_type', 'user_id', 'create_time'),  # 添加复合索引
    )

    id = db.Column(db.Integer, primary_key=True)
    strategy_details_id = db.Column(db.Integer, comment='策略详情id')
    strategy_type = db.Column(db.Integer, comment='策略类型')
    code = db.Column(db.String(20), comment='股票代码')
    name = db.Column(db.String(50), comment='股票名称')
    zxj = db.Column(db.Float, comment='当前价格')
    next_price_buy = db.Column(db.Float, comment='下一个购买价格')
    suggest_buy_num = db.Column(db.Integer, comment='建议购买数量')
    suggest_buy_amt = db.Column(db.Float, comment='建议购买金额')
    strategy_id = db.Column(db.Integer, comment='策略id')
    strategy_name = db.Column(db.String(50), comment='策略名称')
    cost_price = db.Column(db.Float, comment='成本价格')
    hold_number = db.Column(db.Integer, comment='持仓数量')
    income_rate = db.Column(db.String(50), comment='当前收益率')
    hold_amt_after = db.Column(db.Float, comment='买入后持仓金额')
    hold_num_after = db.Column(db.Integer, comment='买入后持仓数量')
    price_after = db.Column(db.Float, comment='买入后持仓价格')
    income_rate_after = db.Column(db.String(50), comment='买入后收益率')
    suggest_sale_num = db.Column(db.Integer, comment='建议卖出数量')
    suggest_sale_amt = db.Column(db.Float, comment='建议卖出金额')
    income_amt = db.Column(db.Float, comment='收益金额')
    user_id = db.Column(db.Integer, comment='用户id')
    is_send = db.Column(db.Integer, comment='是否发送')
    msg_type = db.Column(db.Integer, comment='消息类型:0买入,1卖出')
    create_time = db.Column(db.DateTime, comment='创建时间')
    update_time = db.Column(db.DateTime, comment='更新时间')

