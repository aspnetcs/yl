# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/1/6 15:55

@mark    :
"""
from flask import Flask, Blueprint
from applications.view.quantify.quantify import route_quantify
from applications.view.quantify.selected import route_quantify_selected

quantify_bp = Blueprint('quantify', __name__, url_prefix='/quantify')


def register_quantify_bps(app: Flask):
    # 注册子蓝图
    quantify_bp.register_blueprint(route_quantify)
    quantify_bp.register_blueprint(route_quantify_selected)

    app.register_blueprint(quantify_bp)
