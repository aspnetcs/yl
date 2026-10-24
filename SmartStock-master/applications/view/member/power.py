from flask import Blueprint, render_template, request, jsonify

from applications.common import curd
from applications.common.utils.http import success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import MemberPower
from applications.schemas import PowerOutSchema2
from applications.schemas.admin_power import PowerSchema

route_power = Blueprint('power', __name__, url_prefix='/power')


@route_power.get('/')
@authorize("member:power:main")
def index():
    return render_template('member/power/main.html')


@route_power.post('/data')
@authorize("member:power:main")
def data():
    power = MemberPower.query.all()
    res = {
        "data": PowerSchema(many=True).dump(power)
    }
    return jsonify(res)


@route_power.get('/add')
@authorize("member:power:add", log=True)
def add():
    return render_template('member/power/add.html')


@route_power.get('/selectParent')
@authorize("member:power:main", log=True)
def select_parent():
    power = MemberPower.query.all()
    res = curd.model_to_dicts(schema=PowerOutSchema2, data=power)
    res.append({"powerId": 0, "powerName": "顶级权限", "parentId": -1})
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": res

    }
    return jsonify(res)


# 增加
@route_power.post('/save')
@authorize("member:power:add", log=True)
def save():
    req = request.get_json(force=True)
    icon = str_escape(req.get("icon"))
    openType = str_escape(req.get("openType"))
    parentId = str_escape(req.get("parentId"))
    powerCode = str_escape(req.get("powerCode"))
    powerName = str_escape(req.get("powerName"))
    powerType = str_escape(req.get("powerType"))
    powerUrl = str_escape(req.get("powerUrl"))
    sort = str_escape(req.get("sort"))
    power = MemberPower(
        icon=icon,
        open_type=openType,
        parent_id=parentId,
        code=powerCode,
        name=powerName,
        type=powerType,
        url=powerUrl,
        sort=sort,
        enable=1
    )
    r = db.session.add(power)
    db.session.commit()
    return success_api(msg="成功")


# 权限编辑
@route_power.get('/edit/<int:_id>')
@authorize("member:power:edit", log=True)
def edit(_id):
    power = curd.get_one_by_id(MemberPower, _id)
    icon = str(power.icon).split()
    if len(icon) == 2:
        icon = icon[1]
    else:
        icon = None
    return render_template('member/power/edit.html', power=power, icon=icon)


# 权限更新
@route_power.put('/update')
@authorize("member:power:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = request.get_json(force=True).get("powerId")
    data = {
        "icon": str_escape(req_json.get("icon")),
        "open_type": str_escape(req_json.get("openType")),
        "parent_id": str_escape(req_json.get("parentId")),
        "code": str_escape(req_json.get("powerCode")),
        "name": str_escape(req_json.get("powerName")),
        "type": str_escape(req_json.get("powerType")),
        "url": str_escape(req_json.get("powerUrl")),
        "sort": str_escape(req_json.get("sort"))
    }
    res = MemberPower.query.filter_by(id=id).update(data)
    db.session.commit()
    if not res:
        return fail_api(msg="更新权限失败")
    return success_api(msg="更新权限成功")


# 启用权限
@route_power.put('/enable')
@authorize("member:power:edit", log=True)
def enable():
    _id = request.get_json(force=True).get('powerId')
    if id:
        res = curd.enable_status(MemberPower, _id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启用成功")
    return fail_api(msg="数据错误")


# 禁用权限
@route_power.put('/disable')
@authorize("member:power:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('powerId')
    if id:
        res = curd.disable_status(MemberPower, _id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")


# 权限删除
@route_power.delete('/remove/<int:id>')
@authorize("member:power:remove", log=True)
def remove(id):
    power = MemberPower.query.filter_by(id=id).first()
    power.role = []

    r = MemberPower.query.filter_by(id=id).delete()
    db.session.commit()
    if r:
        return success_api(msg="删除成功")
    else:
        return fail_api(msg="删除失败")
