from flask import Blueprint, render_template, request, jsonify, json

from applications.common.curd import enable_status, disable_status, get_one_by_id
from applications.common.utils.http import table_api, success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.common.libs.jsonformat import r
from applications.models import MemberRole, MemberPower, MemberUser
from applications.schemas import RoleOutSchema, PowerOutSchema2

route_role = Blueprint('role', __name__, url_prefix='/role')


# 用户管理@route_role
@route_role.get('/')
@authorize("member:role:main")
def main():
    return render_template('member/role/main.html')


# 表格数据
@route_role.get('/data')
@authorize("member:role:main")
def table():
    role_name = str_escape(request.args.get('roleName', type=str))
    role_code = str_escape(request.args.get('roleCode', type=str))
    filters = []
    if role_name:
        filters.append(MemberRole.name.contains(role_name))
    if role_code:
        filters.append(MemberRole.code.contains(role_code))
    roles = MemberRole.query.filter(*filters).layui_paginate()
    return table_api(data=RoleOutSchema(many=True).dump(roles), count=roles.total)


# 角色增加
@route_role.get('/add')
@authorize("member:role:add", log=True)
def add():
    return render_template('member/role/add.html')


# 角色增加
@route_role.post('/save')
@authorize("member:role:add", log=True)
def save():
    req = request.get_json(force=True)
    details = str_escape(req.get("details"))
    enable = str_escape(req.get("enable"))
    roleCode = str_escape(req.get("roleCode"))
    roleName = str_escape(req.get("roleName"))
    sort = str_escape(req.get("sort"))
    role = MemberRole(
        details=details,
        enable=enable,
        code=roleCode,
        name=roleName,
        sort=sort
    )
    db.session.add(role)
    db.session.commit()
    return success_api(msg="成功")


# 角色授权
@route_role.get('/power/<int:_id>')
@authorize("member:role:power", log=True)
def power(_id):
    return render_template('member/role/power.html', id=_id)


# 获取角色权限
@route_role.get('/getRolePower/<int:id>')
@authorize("member:role:main", log=True)
def get_role_power(id):
    role = MemberRole.query.filter_by(id=id).first()
    check_powers = role.power
    check_powers_list = []
    for cp in check_powers:
        check_powers_list.append(cp.id)
    powers = MemberPower.query.all()
    power_schema = PowerOutSchema2(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = power_schema.dump(powers)  # 生成可序列化对象
    for i in output:
        if int(i.get("powerId")) in check_powers_list:
            i["checkArr"] = "1"
        else:
            i["checkArr"] = "0"
    res = {
        "data": output,
        "status": {"code": 200, "message": "默认"}
    }
    return jsonify(res)


# 保存角色权限
@route_role.put('/saveRolePower')
@authorize("member:role:edit", log=True)
def save_role_power():
    req_form = request.form
    power_ids = req_form.get("powerIds")
    power_list = power_ids.split(',')
    role_id = req_form.get("roleId")
    role = MemberRole.query.filter_by(id=role_id).first()

    powers = MemberPower.query.filter(MemberPower.id.in_(power_list)).all()
    role.power = powers

    db.session.commit()
    return success_api(msg="授权成功")


# 角色编辑
@route_role.get('/edit/<int:id>')
@authorize("member:role:edit", log=True)
def edit(id):
    r = get_one_by_id(model=MemberRole, id=id)
    return render_template('member/role/edit.html', role=r)


# 更新角色
@route_role.put('/update')
@authorize("member:role:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = req_json.get("roleId")
    data = {
        "code": str_escape(req_json.get("roleCode")),
        "name": str_escape(req_json.get("roleName")),
        "sort": str_escape(req_json.get("sort")),
        "enable": str_escape(req_json.get("enable")),
        "details": str_escape(req_json.get("details"))
    }
    role = MemberRole.query.filter_by(id=id).update(data)
    db.session.commit()
    if not role:
        return fail_api(msg="更新角色失败")
    return success_api(msg="更新角色成功")


# 启用用户
@route_role.put('/enable')
@authorize("member:role:edit", log=True)
def enable():
    id = request.get_json(force=True).get('roleId')
    if id:
        res = enable_status(MemberRole, id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用用户
@route_role.put('/disable')
@authorize("member:role:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('roleId')
    if _id:
        res = disable_status(MemberRole, _id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")


# 角色删除
@route_role.delete('/remove/<int:id>')
@authorize("member:role:remove", log=True)
def remove(id):
    role = MemberRole.query.filter_by(id=id).first()
    # 删除该角色的权限和用户
    role.power = []
    role.user = []

    r = MemberRole.query.filter_by(id=id).delete()
    db.session.commit()
    if not r:
        return fail_api(msg="角色删除失败")
    return success_api(msg="角色删除成功")


# 角色-用户列表
@route_role.get('/users')
@authorize("member:role:users", log=True)
def users():
    role_id = request.values.get('role_id')
    role = get_one_by_id(model=MemberRole, id=role_id)

    user_dicts = []  # 使用更清晰的变量名来表示这是一个用户字典列表
    if role:
        # 假设关系属性名为users，且MemberUser模型有id和last_name字段
        users_with_this_role = role.user
        for user in users_with_this_role:
            user_dict = {"id": user.id, "name": user.last_name}
            # print(user_dict)
            user_dicts.append(user_dict)
    else:
        print('Role not found')

    # 返回渲染的模板，使用更清晰的模板变量名
    return render_template('member/role/users.html', users=user_dicts, role=role)


# 角色-添加用户
@route_role.post('/usersUpdate')
# @authorize("member:role:users", log=True)
def usersUpdate():
    role_id = request.values.get('role_id')

    data = request.get_data()
    j_data = json.loads(data)
    # print(j_data['selectedUserIds'], j_data['unselectedUserIds'])

    if j_data['description']:
        # 新增
        description = j_data['description'].replace('\\n', '').strip()
        user_ids = [uid.strip() for uid in description.split(',')]
    else:
        user_ids = j_data['selectedUserIds']
    # print(user_ids)

    # 从数据库中查询所有MemberUser实例，并提取ID到一个集合中
    member_ids = {mu.id for mu in db.session.query(MemberUser).all()}

    # 分离有效和无效用户
    in_user = [uid for uid in user_ids if uid in member_ids]
    not_in_user = [uid for uid in user_ids if uid not in member_ids]
    # print(in_user, not_in_user)

    # 初始化 found_match 变量
    found_match = False
    # 添加用户角色
    for i in in_user:
        u = MemberUser.query.filter_by(id=i).first()
        for role in u.role:
            # print(role.id)
            # print(role_id)
            if int(role.id) == int(role_id):
                found_match = True

        if not found_match:
            new_role = MemberRole.query.filter(MemberRole.id == role_id).first()
            u.role.append(new_role)

            db.session.commit()

        found_match = False

    # 删除用户角色
    if len(j_data['unselectedUserIds']) > 0:
        for i in j_data['unselectedUserIds']:
            u = MemberUser.query.filter_by(id=i).first()
            if u:
                remove_role = MemberRole.query.filter(MemberRole.id == role_id).first()
                u.role.remove(remove_role)
                # 提交更改到数据库
                db.session.commit()

    return r({}, 0, '修改成功')
