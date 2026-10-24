# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 13:34

@mark    :
"""
import datetime
from flask_login import current_user
from applications.extensions import db
from applications.common.libs.jsonformat import r
from flask import Blueprint, render_template, request, json
from applications.models.system.admin_user import User
from applications.models.stock.StocksStrategy import StocksStrategy
from applications.models.stock.StocksStrategyDetails import StocksStrategyDetails
from applications.models.stock.StocksSelected import StocksSelected

route_details = Blueprint('details', __name__, url_prefix='/details')


@route_details.get('/')
def main():
    return render_template('strategy/details/main.html')


@route_details.get('/list')
def details_list():
    """
    获取策略明细列表
    :return:
    """
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    code = request.values.get('code')
    name = request.values.get('name')

    # 数据库响应
    db_tc = db.session.query(StocksStrategyDetails).filter_by(user_id=current_user.id) \
        .order_by(StocksStrategyDetails.id.desc())
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = [StocksStrategyDetails.id > 0]
    if code:
        where.append(StocksStrategyDetails.code.like("%" + code + "%"))
    if name:
        where.append(StocksStrategyDetails.name.like("%" + name + "%"))

    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()
    count = db_tc.filter(*where).count()

    # 返回json
    for t in tc:
        user_name = db.session.query(User.username).filter_by(id=t.user_id).first()
        strategy_name, remarks = db.session.query(StocksStrategy.name, StocksStrategy.remarks).filter_by(id=t.strategy_id).first()
        selected = db.session.query(StocksSelected.hold_number, StocksSelected.cost_price).filter_by(
            id=t.selected_id).first()
        hold_number = selected.hold_number if selected else 0
        cost_price = selected.cost_price if selected else 0

        temp.append({
            'id': t.id,
            'user_name': user_name[0],
            'code': t.code,
            'name': t.name,
            'zxj': round(t.zxj, 2),
            'zdf_stg_%': str(round(t.zdf_stg * 100, 2)) + '%',
            'zdf_stg': round(t.zdf_stg, 2),
            'zde_stg': round(t.zde_stg, 2),
            'next_price_buy': round(t.next_price_buy, 2),
            'income_rate_target_%': str(round(t.income_rate_target * 100, 0)) + "%",
            'income_rate_target': round(t.income_rate_target, 2),
            'income_target': round(t.income_target, 0),
            'next_price_sell': round(t.next_price_sell, 2),
            'is_monitor': t.is_monitor,
            'strategy_id': t.strategy_id,
            'strategy_name': strategy_name,
            'remarks': remarks,
            'created_time': t.created_time,
            'update_time': t.update_time,
            'total_invest_budget': round(t.total_invest_budget, 0),
            'total_invested': round(t.total_invested, 0),
            'selected_id': t.selected_id,
            'suggest_buy_num': round(t.suggest_buy_num, 0),
            'suggest_buy_amt': round(t.suggest_buy_amt, 0),
            'view_price': round(t.view_price, 2),
            'add_fund': round(t.add_fund, 2),
            'hold_number': hold_number,
            'cost_price': cost_price,
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_details.route('/del', methods=['GET'])
def delStrategy():
    """
    # 删除策略
    :return:
    """
    detailsId = request.values.get('id')
    db.session.query(StocksStrategyDetails).filter_by(id=detailsId).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_details.route('/edit')
def edit():
    """
    # 编辑
    :return:
    """
    detailsId = request.values.get('id')
    StrategyDetails = db.session.query(StocksStrategyDetails).filter_by(id=detailsId).first()
    return render_template('strategy/details/edit.html', StrategyDetails=StrategyDetails)


@route_details.route('/editSave', methods=['POST'])
def editSave():
    """
    # 编辑提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)

    tc = db.session.query(StocksStrategyDetails).filter_by(id=j_data['id']).first()

    if j_data['strategy_id']=='1':
        # 金字塔买入法(N%)
        tc.strategy_id = j_data['strategy_id'],
        tc.zdf_stg = j_data['zdf_stg'],
        tc.add_fund = j_data['add_fund'],
        tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()

    elif j_data['strategy_id']=='9':
        # 监控到价策略
        tc.strategy_id = j_data['strategy_id'],
        tc.view_price = j_data['view_price'],
        tc.add_fund = j_data['add_fund'],
        tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()


    return r({}, 0, '修改成功')


@route_details.route('/strategyList', methods=['GET'])
def strategyList():
    """
    # 获取策略列表，用于前端选择
    :return:
    """
    type_name = request.values.get('type')

    if type_name:
        where = [StocksStrategy.type == type_name]
    else:
        where = []

    data = db.session.query(StocksStrategy.id, StocksStrategy.name).filter(*where).filter_by(status=1).order_by(StocksStrategy.id.desc()).all()

    re = []
    for x in data:
        re.append({'label': x[1], 'value': x[0]})
    return r({'options': re})


@route_details.route('/switch', methods=['GET'])
def switch():
    """
    # switch开关
    :return:
    """
    uid = request.values.get('id')
    is_monitor = request.values.get('is_monitor')

    tc = db.session.query(StocksStrategyDetails).filter_by(id=uid).first()

    if is_monitor == 'false':
        tc.is_monitor = 0
    else:
        tc.is_monitor = 1

    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    db.session.commit()

    return r({}, 0, '修改成功')
