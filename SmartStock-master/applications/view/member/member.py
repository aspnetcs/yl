# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, render_template, request, json
from applications.common import curd
from applications.models.member.MemberUser import MemberUser
from applications.models.member.MemberRole import MemberRole
from applications.extensions import db
from applications.common.libs.jsonformat import r

route_member = Blueprint('member', __name__, url_prefix='/member')


@route_member.get('/')
# @authorize("project:project:main", log=True)
def main():
    return render_template('member/member/main.html')


@route_member.get('/list')
# @authorize("project:project:main", log=True)
def member_list():
    # 接口请求
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    id = request.values.get('id')
    last_name = request.values.get('last_name')

    # 数据库响应
    count = db.session.query(MemberUser).count()
    db_tc = db.session.query(MemberUser).order_by(MemberUser.id.desc())  # 按id降序排序
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = [MemberUser.id > 0]
    if id:
        where.append(MemberUser.id.like("%" + id + "%"))
    if last_name:
        where.append(MemberUser.last_name.like("%" + last_name + "%"))

    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()

    # 返回json
    for t in tc:
        temp.append({
            'id': t.id,
            'last_name': t.last_name,
            'mobile': t.mobile,
            'belong_unit_org_name': t.belong_unit_org_name,
            'dept_org_one': t.dept_org_one,
            'dept_org_two': t.dept_org_two,
            'org_name': t.org_name,
            'post_name': t.post_name,
            'identity': t.identity,
            'status': t.status
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


# 编辑
@route_member.route('/edit')
# @authorize("project:datasource:edit", log=True)
def edit():
    member_id = request.values.get('id')

    user = curd.get_one_by_id(MemberUser, member_id)
    roles = MemberRole.query.all()
    checked_roles = []
    for r in user.role:
        checked_roles.append(r.id)
    return render_template('member/member/edit.html', user=user, roles=roles, checked_roles=checked_roles)


# 编辑提交
@route_member.route('/editSave', methods=['POST'])
# @authorize("project:project:main", log=True)
def editSave():
    data = request.get_data()
    j_data = json.loads(data)

    tc = db.session.query(MemberUser).filter_by(id=j_data['id']).first()
    tc.status = j_data['status']
    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()

    # 用户角色
    u = MemberUser.query.filter_by(id=j_data['id']).first()
    role_ids = j_data['roleIds'].split(',')
    roles = MemberRole.query.filter(MemberRole.id.in_(role_ids)).all()
    u.role = roles

    db.session.commit()

    return r({}, 0, '修改成功')
