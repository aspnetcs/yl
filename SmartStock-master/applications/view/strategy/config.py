# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 13:34

@mark    :
"""
import datetime
from flask import Blueprint, render_template, request, json
from flask_login import current_user
from applications.models.stock.StocksStrategy import StocksStrategy
from applications.extensions import db
from applications.common.libs.jsonformat import r

route_config = Blueprint('config', __name__, url_prefix='/config')


@route_config.get('/')
def main():

    return render_template('strategy/config/main.html')


@route_config.get('/list')
def config_list():
    """
    获取策略列表
    :return:
    """
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    symbol = request.values.get('id')
    name = request.values.get('name')

    # 数据库响应
    count = db.session.query(StocksStrategy).count()

    db_tc = db.session.query(StocksStrategy).order_by(StocksStrategy.id.desc())
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = [StocksStrategy.id > 0]
    if name:
        where.append(StocksStrategy.name.like("%" + name + "%"))

    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()

    # 返回json
    for t in tc:

        temp.append({
            'id': t.id,
            'name': t.name,
            'remarks': t.remarks,
            'status': t.status,
            'created_time': t.created_time,
            'update_time': t.update_time,
            'type': t.type,
            'type_name': '个股' if t.type == 0 else '单笔交易',
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_config.route('/add')
def add():
    """
    # 添加策略
    :return:
    """
    return render_template('strategy/config/add.html')


@route_config.route('/addSave', methods=['POST'])
def addSave():
    """
    # 添加提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)
    # print(j_data)

    project = db.session.query(StocksStrategy.name).filter_by(name=j_data['name'], user_id=current_user.id).first()
    if project is not None:
        return r({}, 0, '', '策略已存在')

    tc = StocksStrategy(
        name=j_data['name'],
        remarks=j_data['remarks'],
        user_id=current_user.id,
        type = j_data['type']
    )
    db.session.add(tc)
    db.session.commit()

    return r({}, 0, '添加成功')


@route_config.route('/del', methods=['GET'])
def delProject():
    """
    # 删除自选
    :return:
    """
    configId = request.values.get('id')
    db.session.query(StocksStrategy).filter_by(id=configId).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_config.route('/delAll', methods=['DELETE'])
def delAll():
    """
    # 批量删除
    :return:
    """
    configId = request.values.get('configId')
    configId = configId.split(',')
    db.session.query(StocksStrategy).filter(StocksStrategy.id.in_(configId)).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_config.route('/edit')
def edit():
    """
    # 编辑
    :return:
    """
    configId = request.values.get('id')
    Strategy = db.session.query(StocksStrategy).filter_by(id=configId).first()
    return render_template('strategy/config/edit.html', Strategy=Strategy)


@route_config.route('/editSave', methods=['POST'])
def editSave():
    """
    # 编辑提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)

    project = db.session.query(StocksStrategy.name).filter_by(name=j_data['name'], user_id=current_user.id).filter(
        StocksStrategy.id != j_data['id']).first()

    if project is not None:
        return r({}, 0, '', '策略已存在')

    tc = db.session.query(StocksStrategy).filter_by(id=j_data['id']).first()
    tc.name = j_data['name']
    tc.remarks = j_data['remarks']
    tc.type = j_data['type']
    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

    db.session.commit()
    return r({}, 0, '修改成功')


@route_config.route('/switch', methods=['GET'])
def switch():
    """
    # switch开关
    :return:
    """
    uid = request.values.get('id')
    status = request.values.get('status')

    tc = db.session.query(StocksStrategy).filter_by(id=uid).first()

    if status == 'false':
        tc.status = 0
    else:
        tc.status = 1

    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    db.session.commit()

    return r({}, 0, '修改成功')
