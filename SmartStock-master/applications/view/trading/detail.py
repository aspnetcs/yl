# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/24 15:38

@mark    :
"""
import datetime
from flask_login import current_user
from applications.extensions import db
from applications.common.libs.jsonformat import r
from flask import Blueprint, render_template, request, json
from applications.models.system.admin_user import User
from applications.models.stock.StocksStrategy import StocksStrategy
from applications.models.stock.StocksTradingDetails import StocksTradingDetails

route_detail = Blueprint('detail', __name__, url_prefix='/detail')


@route_detail.get('/')
def main():
    return render_template('trading/detail/main.html')


@route_detail.get('/list')
def details_list():
    """
    获取交易明细列表
    :return:
    """
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    code = request.values.get('code')
    name = request.values.get('name')
    trade_type = request.values.get('trade_type')
    start_time = request.values.get('start')
    end_time = request.values.get('end')

    # 数据库响应
    db_tc = db.session.query(StocksTradingDetails).filter_by(user_id=current_user.id) \
        .order_by(StocksTradingDetails.trade_time.desc())
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = [StocksTradingDetails.id > 0]
    if code:
        where.append(StocksTradingDetails.code.like("%" + code + "%"))
    if name:
        where.append(StocksTradingDetails.name.like("%" + name + "%"))
    if trade_type:
        where.append(StocksTradingDetails.trade_type == trade_type)
    if start_time:
        where.append(StocksTradingDetails.trade_time >= start_time)
    if end_time:
        where.append(StocksTradingDetails.trade_time <= end_time)

    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()
    count = db_tc.filter(*where).count()

    # 返回json
    for t in tc:
        user_name = db.session.query(User.username).filter_by(id=t.user_id).first()
        strategy_name = db.session.query(StocksStrategy.name).filter_by(id=t.strategy_id).first()
        temp.append({
            'id': t.id,
            'user_name': user_name[0],
            'code': t.code,
            'name': t.name,
            'trade_time': t.trade_time,
            'trade_type': t.trade_type,
            'cjsl': round(t.cjsl, 0),
            'cjjg': round(t.cjjg, 2),
            'jyje': round(t.jyje, 2),
            'strategy_id': t.strategy_id,
            'strategy_name': strategy_name[0],
            'is_monitor': t.is_monitor,
            'zdf_tg': round(t.zdf_tg, 3),
            'zdf_tg_%': str(round(t.zdf_tg * 100, 2)) + '%',
            'next_price_buy': round(t.next_price_buy, 2) if t.next_price_buy else '-',
            'next_price_sell': round(t.next_price_sell, 2) if t.next_price_sell else '-',
            'zxj': t.zxj,
            'zdf': round(((t.zxj - t.cjjg) / t.cjjg) * 100, 2) if t.zxj else '',
            'zdf_str': str(round(((t.zxj - t.cjjg) / t.cjjg) * 100, 2)) + '%' if t.zxj else '',
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_detail.route('/del', methods=['GET'])
def delDetail():
    """
    # 删除交易记录
    :return:
    """
    detailsId = request.values.get('id')
    db.session.query(StocksTradingDetails).filter_by(id=detailsId).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_detail.route('/switch', methods=['GET'])
def switch():
    """
    # switch开关
    :return:
    """
    uid = request.values.get('id')
    is_monitor = request.values.get('is_monitor')

    tc = db.session.query(StocksTradingDetails).filter_by(id=uid).first()

    if is_monitor == 'false':
        tc.is_monitor = 0
    else:
        tc.is_monitor = 1

    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    db.session.commit()

    return r({}, 0, '修改成功')


@route_detail.route('/edit')
def edit():
    """
    # 编辑
    :return:
    """
    return render_template('trading/detail/edit.html')


@route_detail.route('/editSave', methods=['POST'])
def editSave():
    """
    # 编辑提交
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)
    # print(j_data)

    tc = db.session.query(StocksTradingDetails).filter_by(id=j_data['id']).first()
    tc.name = j_data['name'],
    tc.trade_time = j_data['trade_time'],
    tc.trade_type = j_data['trade_type'],
    tc.cjsl = j_data['cjsl'],
    tc.cjjg = j_data['cjjg'],
    tc.jyje = float(j_data['cjsl']) * float(j_data['cjjg']),
    tc.strategy_id = j_data['strategy_id'],
    tc.zdf_tg = j_data['zdf_tg'],
    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db.session.commit()
    return r({}, 0, '修改成功')
