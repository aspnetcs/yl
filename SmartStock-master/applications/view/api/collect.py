# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/12/9 9:45 

@mark    :
'''
from flask import Blueprint, request, jsonify, g, json
from applications.common.libs.Helper import getCurrentDate
from applications.common.utils.http import success_api, fail_api
from applications.common.libs.member.MemberService import MemberService
from applications.models.member.MemberUser import MemberUser
from applications.models.member.MemberPower import MemberPower
from applications.models.member.MemberCollection import MemberCollection
from applications.extensions import db

route_api_collect = Blueprint('collect', __name__, url_prefix='/collect')


# 收藏列表
@route_api_collect.route('/list', methods=['GET'])
def collect_list():
    reqs = {'code': 200, 'msg': '获取成功', 'data': {}}

    # 获取用户信息
    user_id = request.values.get('user_id')
    collect_type = request.values.get('collect_type')
    # print(req)

    tc = db.session.query(MemberCollection).filter_by(member_id=user_id, collect_type=collect_type).all()
    clt_list = []
    if tc:
        for i in tc:
            clt_list.append(i.power_id)

    report = MemberPower.query.filter(MemberPower.id.in_(clt_list)).all()
    # 返回json
    temp = []
    for t in report:
        temp.append({
            'id': t.id,
            'title': t.name,
            'type': t.type,
            'code': t.code,
            'href': t.url,
            'open_type': t.open_type,
            'parent_id': t.parent_id,
            'icon': t.icon,
            'sort': t.sort
        })
    reqs["data"] = temp

    return jsonify(reqs)


# 添加收藏
@route_api_collect.route('/add', methods=['POST'])
def collect_add():
    reqs = {'code': 200, 'msg': '添加成功'}

    # 获取用户信息
    data = request.get_data()
    req = json.loads(data)
    # print(req)

    try:
        if req["collect_type"] == 1:
            model_collect = MemberCollection()
            model_collect.member_id = req["user_id"]
            model_collect.power_id = req["report_id"]
            model_collect.collect_type = req["collect_type"]
            model_collect.created_time = getCurrentDate()
            db.session.add(model_collect)
            db.session.commit()
        else:
            tc = db.session.query(MemberCollection).filter_by(member_id=req["user_id"], collect_type=0).first()
            if tc:
                tc.member_id = req["user_id"]
                tc.power_id = req["report_id"]
                tc.created_time = getCurrentDate()
                db.session.commit()
            else:
                model_collect = MemberCollection()
                model_collect.member_id = req["user_id"]
                model_collect.power_id = req["report_id"]
                model_collect.collect_type = req["collect_type"]
                model_collect.created_time = getCurrentDate()
                db.session.add(model_collect)
                db.session.commit()
    except Exception as e:
        return jsonify({'code': 500, 'msg': '添加失败', "data": str(e)})

    return jsonify(reqs)


# 取消收藏
@route_api_collect.route('/cancel', methods=['POST'])
def collect_cancel():
    reqs = {'code': 200, 'msg': '取消成功'}

    # 获取用户信息
    data = request.get_data()
    req = json.loads(data)
    # print(req)

    r = MemberCollection.query.filter_by(power_id=req["report_id"], member_id=req["user_id"], collect_type=1).delete()
    db.session.commit()
    if not r:
        reqs["code"] = 500
        reqs["msg"] = "取消失败"
        return jsonify(reqs)
    return jsonify(reqs)
