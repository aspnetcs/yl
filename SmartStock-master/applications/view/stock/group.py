# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 13:34

@mark    :
"""
import datetime
from flask import Blueprint, render_template, request, json
from flask_login import current_user
from applications.models.stock.StocksGroup import StocksGroup
from applications.models.system.admin_user import User
from applications.extensions import db
from applications.common.libs.jsonformat import r, build_tree

route_group = Blueprint('group', __name__, url_prefix='/group')


@route_group.get('/')
def main():
    return render_template('stock/group/main.html')


@route_group.route('/list')
def getGroup():
    """
    # 获取列表
    :return:
    """
    # 接口请求
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    name = request.values.get('name')

    # 数据库响应
    count = db.session.query(StocksGroup).filter_by(user_id=current_user.id).count()
    db_tc = db.session.query(StocksGroup).filter_by(user_id=current_user.id).order_by(StocksGroup.id.desc())  # 按id降序排序
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = [StocksGroup.id > 0]
    if name:
        where.append(StocksGroup.name.like("%" + name + "%"))

    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()

    # 返回json
    for t in tc:
        username = db.session.query(User.username).filter_by(id=t.user_id).first()  # 获取用户id
        if t.parent_id == 0:  # 获取父级项目
            parent_name = ''
        else:
            parent_name = db.session.query(StocksGroup.name).filter_by(id=t.parent_id).first()
            parent_name = parent_name[0]
        temp.append({
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'username': username[0],
            'flag': t.flag,
            'create_time': str(t.create_time),
            'update_time': t.update_time,
            'parent_name': parent_name,
            'parent_id': t.parent_id,
            'stocks_type': t.stocks_type
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_group.route('/add')
def add():
    """
    # 增加
    :return:
    """
    return render_template('stock/group/add.html')


@route_group.route('/addSave', methods=['POST'])
def addSave():
    """
    # 新增提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)

    if j_data['group_id']:
        parent_id = j_data['group_id']
    else:
        parent_id = 0

    group = db.session.query(StocksGroup.name, StocksGroup.parent_id).filter_by(name=j_data['name']
                                                                                , user_id=current_user.id).first()
    if group is not None:
        if (j_data['name'], int(parent_id)) in group:
            return r({}, 0, '', '分组已存在')

    tc = StocksGroup(j_data['name'], j_data['description'], current_user.id, j_data['flag']
                     , datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     parent_id, 0, j_data['stocks_type'])
    db.session.add(tc)
    db.session.commit()

    return r({}, 0, '添加成功')


@route_group.route('/edit')
def edit():
    """
    # 编辑
    :return:
    """
    return render_template('stock/group/edit.html')


@route_group.route('/editSave', methods=['PUT'])
def editSave():
    """
    # 编辑提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)

    if j_data['project_id']:
        parent_id = j_data['project_id']
    else:
        parent_id = 0

    project = db.session.query(StocksGroup.name, StocksGroup.parent_id).filter_by(name=j_data['name']
                                                                                  , user_id=current_user.id).filter(
        StocksGroup.id != j_data['id']).first()
    if project is not None:
        if (j_data['name'], int(parent_id)) in project:
            return r({}, 0, '', '分组已存在')

    tc = db.session.query(StocksGroup).filter_by(id=j_data['id']).first()
    tc.name = j_data['name'],
    tc.description = j_data['description'],
    tc.flag = j_data['flag'],
    tc.parent_id = parent_id,
    tc.stocks_type = j_data['stocks_type']
    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

    db.session.commit()
    return r({}, 0, '修改成功')


@route_group.route('/del', methods=['GET'])
def delProject():
    """
    # 删除
    :return:
    """
    groupId = request.values.get('groupId')
    db.session.query(StocksGroup).filter_by(id=groupId).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_group.route('/delall', methods=['DELETE'])
def delAllProject():
    """
    # 批量删除
    :return:
    """
    groupId = request.values.get('groupId')
    groupId = groupId.split(',')
    db.session.query(StocksGroup).filter(StocksGroup.id.in_(groupId)).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_group.route('/is_top', methods=['GET'])
def is_top():
    """
    # switch开关
    :return:
    """
    uid = request.values.get('id')
    top_status = request.values.get('is_top')

    tc = db.session.query(StocksGroup).filter_by(id=uid).first()

    tc.is_top = top_status

    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    db.session.commit()

    return r({}, 0, '修改成功')


@route_group.route('/belong_project', methods=['GET'])
def belong_project():
    """
    # 归属项目下拉树
    :return:
    """
    # 数据库响应
    db_tc = db.session.query(StocksGroup).filter_by(user_id=current_user.id).order_by(StocksGroup.name.desc())  # 按id降序排序
    temp = []
    where = [StocksGroup.id > 0]

    tc = db_tc.filter(*where).all()

    # 返回json
    for t in tc:
        temp.append({
            'id': t.id,
            'title': t.name,
            'checkArr': 0,
            'parentId': t.parent_id
        })

    data_tree = build_tree(temp)

    return r(data_tree)
