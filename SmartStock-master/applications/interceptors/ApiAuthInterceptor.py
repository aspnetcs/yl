from flask import request, jsonify, g
from applications.config import BaseConfig
from applications.models.member.MemberUser import MemberUser
from applications.common.libs.member.MemberService import MemberService

import re

"""
API认证
"""


def before_request():
    api_ignore_urls = BaseConfig.API_IGNORE_URLS
    path = request.path
    # print(path)
    # 只拦截/api来源
    if 'api' not in path:
        return
    # print('是否登录')
    # 是否登录 check_member_login()
    member_info = check_member_login()
    g.member_info = None
    if member_info:
        g.member_info = member_info

    pattern = re.compile('%s' % "|".join(api_ignore_urls))
    if pattern.match(path):
        return

    if not member_info:
        resp = {'code': -1, 'msg': '未登录~', 'data': {}}
        return jsonify(resp)

    return


"""
判断用户是否登录
"""


def check_member_login():
    auth_cookie = request.headers.get('Authorization')
    # print(auth_cookie)
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        member_info = MemberUser.query.filter_by(id=auth_info[1]).first()
    except Exception:
        return False

    if member_info is None:
        return False

    if auth_info[0] != MemberService.geneAuthCode(member_info):
        return False

    if member_info.status != 1:
        return False

    return member_info
