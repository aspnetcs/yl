# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/3/19 13:04

@mark    :
"""
from flask import Blueprint, session, request, json, jsonify
from flask_login import current_user, login_user
from applications.common.admin_log import login_log
from applications.common.utils.http import fail_api, success_api
from applications.models import User
from applications.common.libs.member.MemberService import MemberService


route_api_login = Blueprint('login', __name__, url_prefix='/login')


@route_api_login.post('/login')
def member_login():
    """
    # 登录
    :return:
    """
    reqs = {'code': 200, 'msg': '登录成功', 'data': {}}

    data = request.get_data()
    req = json.loads(data)
    username = req.get('username')
    password = req.get('password')

    if not username or not password:
        reqs['code'] = 500
        reqs['msg'] = '用户名或密码没有输入'
        return jsonify(reqs)

    user = User.query.filter_by(username=username).first()

    if not user:
        reqs['code'] = 500
        reqs['msg'] = '不存在的用户'
        return jsonify(reqs)

    if user.enable == 0:
        reqs['code'] = 500
        reqs['msg'] = '用户被暂停使用'
        return jsonify(reqs)

    if username == user.username and user.validate_password(password):
        # 登录
        login_user(user)
        # 记录登录日志
        login_log(request, uid=user.id, is_access=True)
        # 授权路由存入session
        role = current_user.role
        user_power = []
        for i in role:
            if i.enable == 0:
                continue
            for p in i.power:
                if p.enable == 0:
                    continue
                user_power.append(p.code)
        session['permissions'] = user_power

        # token是Cookie
        token = "%s#%s" % (MemberService.geneAuthCode2(user), user.id)

        reqs['data'] = {"token": token}
        return jsonify(reqs)

    login_log(request, uid=user.id, is_access=False)

    reqs['code'] = 500
    reqs['msg'] = '用户名或密码错误'

    return jsonify(reqs)


@route_api_login.route('/check_reg', methods=['POST'])
def member_check_reg():
    """
    # 判断是否是注册过的用户
    :return:
    """
    reqs = {'code': 200, 'msg': '登录成功', 'data': {}}

    # 获取用户信息
    data = request.get_data()
    req = json.loads(data)
    # print(req)

    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        reqs['code'] = 500
        reqs['msg'] = '需要code'
        return jsonify(reqs)

    # 获取openid
    openid = MemberService.getWeChatOpenid(code)
    if openid is None:
        reqs['code'] = -1
        reqs['msg'] = '需要openid'
        return jsonify(reqs)

    # 根据openid校验是否绑定
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        reqs['code'] = -1
        reqs['msg'] = '未绑定'
        return jsonify(reqs)

    # 校验是否公司用户
    member_info = MemberUser.query.filter_by(id=bind_info.member_id, status=1).first()

    if not member_info:
        reqs['code'] = -1
        reqs['msg'] = '非公司内部用户，禁止访问'
        return jsonify(reqs)

    # token是Cookie
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)

    reqs['data'] = {"token": token}
    return jsonify(reqs)