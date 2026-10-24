from flask import Flask, Blueprint

from applications.view.api.Member import route_api_member as api_member_bp
from applications.view.api.rights import route_rights
from applications.view.api.collect import route_api_collect
from applications.view.api.stock import route_api_stock
from applications.view.api.login import route_api_login


# 创建sys
api_bp = Blueprint('api', __name__, url_prefix='/api')


def register_api_bps(app: Flask):
    # 注册子蓝图
    api_bp.register_blueprint(api_member_bp)
    api_bp.register_blueprint(route_rights)
    api_bp.register_blueprint(route_api_collect)
    api_bp.register_blueprint(route_api_stock)
    api_bp.register_blueprint(route_api_login)

    app.register_blueprint(api_bp)


@api_bp.route('/')
def index():
    return "Mina api v1.0"


