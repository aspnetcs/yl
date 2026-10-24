# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 13:34

@mark    :
"""
import datetime
from sqlalchemy import func
from flask import Blueprint, render_template, request, json
from flask_login import current_user
from applications.extensions import db
from applications.common.libs.tool import coalesce
from applications.common.libs.jsonformat import r
from applications.models.stock.StocksSelected import StocksSelected
from applications.models.stock.Stocks import Stocks
from applications.models.stock.StocksStrategyDetails import StocksStrategyDetails
from applications.models.stock.StocksTradingDetails import StocksTradingDetails


route_selected = Blueprint('selected', __name__, url_prefix='/selected')


@route_selected.get('/')
def main():
    update_time = db.session.query(func.max(Stocks.update_time)).scalar()

    return render_template('stock/selected/main.html', updateTime=update_time)


@route_selected.get('/list')
def selected_list():
    """
    获取列表
    :return:
    """
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    symbol = request.values.get('id')
    name = request.values.get('name')
    isHold = request.values.get('isHold')

    # 数据库响应
    count = db.session.query(StocksSelected).filter_by(user_id=current_user.id).count()
    db_tc = db.session.query(StocksSelected).filter_by(user_id=current_user.id).order_by(StocksSelected.id.desc())
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = [StocksSelected.id > 0]
    if symbol:
        where.append(StocksSelected.symbol.like("%" + symbol + "%"))
    if name:
        where.append(StocksSelected.name.like("%" + name + "%"))
    if isHold:
        where.append(StocksSelected.is_hold == isHold)


    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()

    # 返回json
    for t in tc:
        sk = db.session.query(Stocks).filter_by(code=t.code).first()

        temp.append({
            'id': t.id,
            'code': t.code,
            'name': t.name,
            'group_id': t.group_id,
            'is_hold': t.is_hold,
            'is_news': t.is_news,
            'stock_type': t.stock_type,
            'cost_price': round(coalesce(t.cost_price, 0), 3),
            "hold_number": round(coalesce(t.hold_number, 0), 0),
            "zxj": round(coalesce(sk.zxj, 0), 2),
            "zde": round(coalesce(sk.zde, 0), 2),
            "zdf": round(coalesce(sk.zdf, 0), 2),
            "cjl": round(coalesce(sk.cjl, 0), 2),
            "cje": round(coalesce(sk.cje, 0), 2),
            "syl_dt": sk.syl_dt,
            "sjl": sk.sjl,
            "zsz": round(coalesce(sk.zsz, 0), 2),
            "ltsz": round(coalesce(sk.ltsz, 0), 2),
            "zdf_60d": round(coalesce(sk.zdf_60d, 0), 2),
            "zdf_nzj": round(coalesce(sk.zdf_nzj, 0), 2),
            "cost_amt": round(coalesce(t.cost_price * t.hold_number, 0), 0),
            "now_value": round(coalesce(sk.zxj * t.hold_number, 0), 0),
            "profit": round((coalesce(sk.zxj * t.hold_number, 0)) - (coalesce(t.cost_price * t.hold_number, 0)), 0),
            "total_invest_budget": round(coalesce(t.total_invest_budget, 0), 0),
            "income_rate_target": round(coalesce(t.income_rate_target, 0), 2),
            "income_target": round(t.total_invest_budget * t.income_rate_target, 0),
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_selected.route('/del', methods=['GET'])
def delSelected():
    """
    # 删除
    :return:
    """
    selectedId = request.values.get('selectedId')
    db.session.query(StocksSelected).filter_by(id=selectedId).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_selected.route('/delAll', methods=['DELETE'])
def delAll():
    """
    # 批量删除
    :return:
    """
    selectedId = request.values.get('selectedId')
    selectedId = selectedId.split(',')
    db.session.query(StocksSelected).filter(StocksSelected.id.in_(selectedId)).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_selected.route('/edit')
def edit():
    """
    # 编辑
    :return:
    """
    return render_template('stock/selected/edit.html')


@route_selected.route('/editSave', methods=['PUT'])
def editSave():
    """
    # 编辑提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)

    if j_data['group_id']:
        group_id = j_data['group_id']
    else:
        group_id = 0

    if j_data['stock_type']:
        stock_type = j_data['stock_type']
    else:
        stock_type = 0

    tc = db.session.query(StocksSelected).filter_by(id=j_data['id']).first()
    tc.group_id = group_id,
    tc.is_hold = j_data['is_hold'],
    tc.is_news = j_data['is_news'],
    tc.stock_type = stock_type,
    tc.cost_price = j_data['cost_price'],
    tc.hold_number = j_data['hold_number'],
    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    tc.total_invest_budget = j_data['total_invest_budget'],
    tc.income_rate_target = j_data['income_rate_target'],

    db.session.commit()
    return r({}, 0, '修改成功')


@route_selected.route('/strategy')
def strategy():
    """
    # 增加策略
    :return:
    """
    return render_template('stock/selected/addStrategy.html')


@route_selected.route('/strategySave', methods=['POST'])
def strategySave():
    """
    # 增加策略提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)

    if j_data['strategy_id']=='1':
        # 金字塔买入法(N%)
        tc = StocksStrategyDetails(
            user_id=current_user.id,
            code=j_data['code'],
            name=j_data['name'],
            strategy_id=j_data['strategy_id'],
            selected_id=j_data['id'],
            zdf_stg=j_data['zdf_stg'],
            add_fund=j_data['add_fund'],
        )
        db.session.add(tc)
        db.session.commit()

    elif j_data['strategy_id']=='9':
        # 监控到价策略
        tc = StocksStrategyDetails(
            user_id=current_user.id,
            code=j_data['code'],
            name=j_data['name'],
            strategy_id=j_data['strategy_id'],
            selected_id=j_data['id'],
            view_price=j_data['view_price'],
            add_fund=j_data['add_fund'],
        )
        db.session.add(tc)
        db.session.commit()

    return r({}, 0, '添加成功')


@route_selected.route('/trading')
def trading():
    """
    # 增加交易明细
    :return:
    """
    return render_template('stock/selected/addTrading.html')


@route_selected.route('/tradingSave', methods=['POST'])
def tradingSave():
    """
    # 增加交易明细提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)

    tc = StocksTradingDetails(
        user_id=current_user.id,
        code=j_data['code'],
        name=j_data['name'],
        cjsl=j_data['cjsl'],
        cjjg=j_data['cjjg'],
        jyje=float(j_data['cjjg']) * float(j_data['cjsl']),
        strategy_id=j_data['strategy_id'],
        selected_id=j_data['id'],
        zdf_tg=j_data['zdf_tg'],
        trade_time=j_data['trade_time'],
        trade_type=j_data['trade_type']
    )
    db.session.add(tc)
    db.session.commit()

    return r({}, 0, '添加成功')
