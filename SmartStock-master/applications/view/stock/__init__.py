# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/1/6 15:55

@mark    :
"""
from flask import Flask, Blueprint
from applications.view.stock.selected import route_selected
from applications.view.stock.market import route_market
from applications.view.stock.group import route_group
from applications.view.stock.news import route_news

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')


def register_stock_bps(app: Flask):
    # 注册子蓝图
    stock_bp.register_blueprint(route_selected)
    stock_bp.register_blueprint(route_market)
    stock_bp.register_blueprint(route_group)
    stock_bp.register_blueprint(route_news)

    app.register_blueprint(stock_bp)
