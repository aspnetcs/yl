# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 13:34

@mark    :
"""
import datetime
from sqlalchemy import func, and_
from flask import Blueprint, render_template, request, json
from flask_login import current_user
from applications.models.stock.Stocks import Stocks
from applications.models.stock.StocksSelected import StocksSelected
from applications.extensions import db
from applications.common.libs.jsonformat import r

route_market = Blueprint('market', __name__, url_prefix='/market')


@route_market.get('/')
def main():
    update_time = db.session.query(func.max(Stocks.update_time)).scalar()

    return render_template('stock/market/main.html', updateTime=update_time)


@route_market.get('/list')
def market_list():
    """
    获取行情列表
    :return:
    """
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    symbol = request.values.get('id')
    name = request.values.get('name')

    # 数据库响应
    sel_tc = db.session.query(StocksSelected.code).filter_by(user_id=current_user.id).all()
    stock_codes = [code[0] for code in sel_tc]
    # print(stock_codes)
    db_tc = db.session.query(Stocks).filter(Stocks.zxj.isnot(None)).order_by(Stocks.zdf.desc())
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = []
    if symbol:
        where.append(Stocks.code.like("%" + symbol + "%"))
    if name:
        where.append(Stocks.name.like("%" + name + "%"))

    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()
    count = db_tc.filter(*where).count()

    # 返回json
    for t in tc:
        # 是否自选
        if t.code in stock_codes:
            is_selected = 1
        else:
            is_selected = 0

        temp.append({
            'region': t.region,
            'code': t.code,
            'name': t.name,
            'zxj': round(t.zxj, 2),
            'zdf': round(t.zdf, 2),
            'zde': round(t.zde, 2),
            'cjl': str(round(t.cjl / 10000, 2)) + '万',
            'cje': str(round(t.cje / 10000, 2)) + '亿',
            'syl_dt': t.syl_dt,
            'sjl': t.sjl,
            'zsz': str(round(t.zsz, 0)) + '亿',
            'ltsz': str(round(t.ltsz, 0)) + '亿',
            'zdf_60d': str(round(t.zdf_60d, 2)) + '%',
            'zdf_nzj': str(round(t.zdf_nzj, 2)) + '%',
            'is_selected': is_selected
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_market.route('/add')
def add():
    """
    # 添加自选
    :return:
    """
    return render_template('stock/market/add.html')


@route_market.route('/addSave', methods=['POST'])
def addSave():
    """
    # 添加提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)
    # print(j_data)

    if j_data['group_id']:
        group_id = j_data['group_id']
    else:
        group_id = 0

    if j_data['stock_type']:
        stock_type = j_data['stock_type']
    else:
        stock_type = 0

    tc = StocksSelected(
        user_id=current_user.id,
        code=j_data['code'],
        name=j_data['name'],
        group_id=group_id,
        is_hold=j_data['is_hold'],
        stock_type=stock_type,
        cost_price=j_data['cost_price'],
        hold_number=j_data['hold_number'],
        total_invest_budget=0,
        income_rate_target=0,
        created_time=str(datetime.datetime.now())
    )
    db.session.add(tc)
    db.session.commit()

    return r({}, 0, '添加成功')


@route_market.route('/del', methods=['GET'])
def delProject():
    """
    # 删除自选
    :return:
    """
    selectedCode = request.values.get('code')
    db.session.query(StocksSelected).filter_by(code=selectedCode, user_id=current_user.id).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_market.get('/updateTime')
def updateTime():
    """
    股票池stocks更新时间
    :return:
    """
    # 数据库响应
    db_tc = db.session.query(func.max(Stocks.created_time)).scalar()
    print(db_tc)

    return r(db_tc)
