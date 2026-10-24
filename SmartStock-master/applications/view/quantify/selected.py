# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/3/10 09:15

@mark    :
"""
# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 13:34

@mark    :
"""
import datetime
from flask import Blueprint, render_template, request, json
from flask_login import current_user
from applications.models.stock.StocksQuantify import StocksQuantify
from applications.models.system.admin_user import User
from applications.extensions import db
from applications.common.libs.jsonformat import r, build_tree

route_quantify_selected = Blueprint('selected', __name__, url_prefix='/selected')


@route_quantify_selected.get('/')
def main():
    return render_template('quantify/selected/main.html')


@route_quantify_selected.route('/list')
def selected_list():
    """
    # 获取列表
    :return:
    """
    # 接口请求
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    name = request.values.get('name')

    # 数据库响应
    db_tc = db.session.query(StocksQuantify).filter_by(user_id=current_user.id).order_by(StocksQuantify.id.desc())  # 按id降序排序
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = [StocksQuantify.id > 0]
    if name:
        where.append(StocksQuantify.name.like("%" + name + "%"))

    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()
    count = db_tc.filter(*where).count()

    # 返回json
    for t in tc:
        username = db.session.query(User.username).filter_by(id=t.user_id).first()  # 获取用户id
        temp.append({
            'id': t.id,
            'name': t.name,
            'mark': t.mark,
            'username': username[0],
            'update_time': str(t.update_time)
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_quantify_selected.route('/edit')
def edit():
    """
    # 编辑
    :return:
    """
    fit = db.session.query(StocksQuantify).filter_by(id=request.values.get('id')).first()
    filter_data = json.loads(fit.filter)
    # print(filter_data)

    return render_template('quantify/selected/edit.html', filterData=filter_data,id=fit.id,quantifyName=fit.name,quantifyMark=fit.mark)



@route_quantify_selected.route('/editSave', methods=['PUT'])
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


@route_quantify_selected.route('/del', methods=['GET'])
def delProject():
    """
    # 删除
    :return:
    """
    selectedId = request.values.get('selectedId')
    db.session.query(StocksQuantify).filter_by(id=selectedId).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_quantify_selected.route('/delAll', methods=['DELETE'])
def delAll():
    """
    # 批量删除
    :return:
    """
    selectedId = request.values.get('selectedId')
    selectedId = selectedId.split(',')
    db.session.query(StocksQuantify).filter(StocksQuantify.id.in_(selectedId)).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


