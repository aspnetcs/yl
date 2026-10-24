# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/7 8:44

@mark    :
"""
from flask import Flask, Blueprint
from applications.view.trading.detail import route_detail



trading_bp = Blueprint('trading', __name__, url_prefix='/trading')


def register_trading_bps(app: Flask):
    # 注册子蓝图
    trading_bp.register_blueprint(route_detail)

    app.register_blueprint(trading_bp)
