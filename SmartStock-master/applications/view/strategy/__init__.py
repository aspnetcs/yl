# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/7 8:44

@mark    :
"""
from flask import Flask, Blueprint
from applications.view.strategy.config import route_config
from applications.view.strategy.details import route_details


strategy_bp = Blueprint('strategy', __name__, url_prefix='/strategy')


def register_strategy_bps(app: Flask):
    # 注册子蓝图
    strategy_bp.register_blueprint(route_config)
    strategy_bp.register_blueprint(route_details)

    app.register_blueprint(strategy_bp)
