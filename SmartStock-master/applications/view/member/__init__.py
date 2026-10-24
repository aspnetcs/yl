from flask import Flask, Blueprint
from applications.view.member.member import route_member
from applications.view.member.role import route_role
from applications.view.member.power import route_power

# 创建sys
member_bp = Blueprint('member', __name__, url_prefix='/member')


def register_member_bps(app: Flask):
    # 在admin_bp下注册子蓝图
    member_bp.register_blueprint(route_member)
    member_bp.register_blueprint(route_role)
    member_bp.register_blueprint(route_power)

    app.register_blueprint(member_bp)
