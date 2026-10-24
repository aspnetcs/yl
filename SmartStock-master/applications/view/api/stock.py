# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/3/19 08:26

@mark    :
"""
from flask import Blueprint, render_template, request, json
from applications.common.libs.tool import coalesce
from applications.extensions import db
from applications.common.libs.jsonformat import r
from applications.models.stock.StocksSelected import StocksSelected
from applications.models.stock.Stocks import Stocks
from applications.models.system.admin_user import User
from applications.models import StocksNews
from applications.models.stock.StocksStrategy import StocksStrategy
from applications.models.stock.StocksStrategyDetails import StocksStrategyDetails
from applications.models.stock.StocksTradingDetails import StocksTradingDetails


route_api_stock = Blueprint('stock', __name__, url_prefix='/stock')


@route_api_stock.get('/selectedList')
def selected_list():
    """
    获取列表
    :return:
    """
    user_id = request.values.get('user_id')
    code = request.values.get('code')

    # 数据库响应
    db_tc = (db.session.query(StocksSelected).filter_by(user_id=user_id)
          .order_by(StocksSelected.id.desc()))
    rt = {}
    temp = []
    where = [StocksSelected.id > 0]
    if code:
        where.append(StocksSelected.code == code)

    tc = db_tc.filter(*where).all()

    # 返回json
    for t in tc:
        sk = db.session.query(Stocks).filter_by(code=t.code).first()
        # print(sk)
        temp.append({
            'id': t.id,
            'code': t.code,
            'name': t.name,
            'group_id': t.group_id,
            'is_hold': t.is_hold,
            'is_news': t.is_news,
            'stock_type': t.stock_type,
            'cost_price': round(coalesce(t.cost_price,0), 3),
            "hold_number": round(coalesce(t.hold_number,0), 0),
            "zxj": round(coalesce(sk.zxj,0), 2),
            "zde": round(coalesce(sk.zde,0), 2),
            "zdf": round(coalesce(sk.zdf,0), 2),
            "zdf_nzj": round(coalesce(sk.zdf_nzj,0), 2),
            "cost_amt": round(coalesce(t.cost_price * t.hold_number,0), 0),
            "now_value": round(coalesce(sk.zxj * t.hold_number,0), 0),
            "profit": round((coalesce(sk.zxj * t.hold_number,0)) - (coalesce(t.cost_price * t.hold_number,0)), 0),
            "profit_rate": round((((coalesce(sk.zxj * t.hold_number,0)) - (coalesce(t.cost_price * t.hold_number,0))) / (coalesce(t.cost_price * t.hold_number,0))) * 100,0) if t.cost_price * t.hold_number != 0 else 0,
            "update_time": sk.update_time
        })

    # 计算总收益和总收益率
    total_profit = sum(item['profit'] for item in temp)
    total_cost = sum(item['cost_amt'] for item in temp)
    total_profit_rate = round((total_profit / total_cost) * 100, 2) if total_cost != 0 else 0
    max_update_time = max(temp, key=lambda x: x['update_time'])['update_time']

    rt['total_profit'] = total_profit
    rt['total_cost'] = total_cost
    rt['total_profit_rate'] = total_profit_rate
    rt['max_update_time'] = max_update_time

    rt['rows'] = temp

    return r(rt)


@route_api_stock.get('/marketList')
def marketList():
    """
    获取行情列表
    :return:
    """
    pageSize = int(request.values.get('pageSize'))
    pageNo = int(request.values.get('pageNo'))
    searchVal = request.values.get('searchVal')
    userId = request.values.get('userId')

    # 数据库响应
    sel_tc = db.session.query(StocksSelected.code).filter_by(user_id=userId).all()
    stock_codes = [code[0] for code in sel_tc]
    # print(stock_codes)
    db_tc = db.session.query(Stocks).filter(Stocks.zxj.isnot(None)).order_by(Stocks.zdf.desc())
    offset = ((pageNo - 1) * pageSize)
    rt = {}
    temp = []
    where = []
    if searchVal:
        # 添加搜索关键词的模糊查询条件
        where.append(db.or_(Stocks.code.like("%" + searchVal + "%"), Stocks.name.like("%" + searchVal + "%")))

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
            'cje': str(round(t.cje / 100000000, 2)) + '亿',
            'syl_dt': round(t.syl_dt, 2),
            'sjl': round(t.sjl, 2),
            'zsz': str(round(t.zsz / 100000000, 2)) + '亿',
            'ltsz': round(t.ltsz, 2),
            'zdf_60d': str(round(t.zdf_60d, 2)) + '%',
            'zdf_nzj': str(round(t.zdf_nzj, 2)) + '%',
            'is_selected': is_selected
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_api_stock.get('/strategyList')
def strategyList():
    """
    获取策略明细列表
    :return:
    """
    searchVal = request.values.get('searchVal')
    userId = request.values.get('userId')
    id = request.values.get('id')

    # 数据库响应
    count = db.session.query(StocksStrategyDetails).count()

    db_tc = db.session.query(StocksStrategyDetails).filter_by(user_id=userId) \
        .order_by(StocksStrategyDetails.id.desc())
    rt = {}
    temp = []
    where = [StocksStrategyDetails.id > 0]

    if searchVal:
        # 添加搜索关键词的模糊查询条件
        where.append(db.or_(StocksStrategyDetails.code.like("%" + searchVal + "%"), StocksStrategyDetails.name.like("%" + searchVal + "%")))

    if id:
        where.append(StocksStrategyDetails.id == id)

    tc = db_tc.filter(*where).all()

    # 返回json
    for t in tc:
        user_name = db.session.query(User.username).filter_by(id=t.user_id).first()
        strategy_name = db.session.query(StocksStrategy.name).filter_by(id=t.strategy_id).first()
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
            'strategy_name': strategy_name[0],
            'created_time': t.created_time,
            'update_time': t.update_time,
            'total_invest_budget': round(t.total_invest_budget, 0),
            'total_invested': round(t.total_invested, 0),
            'selected_id': t.selected_id,
            'suggest_buy_num': round(t.suggest_buy_num, 0),
            'suggest_buy_amt': round(t.suggest_buy_amt, 0)
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_api_stock.get('/tradingList')
def tradingList():
    """
    获取交易明细列表
    :return:
    """
    searchVal = request.values.get('searchVal')
    userId = request.values.get('userId')
    id = request.values.get('id')

    # 数据库响应
    count = db.session.query(StocksTradingDetails).count()

    db_tc = db.session.query(StocksTradingDetails).filter_by(user_id=userId) \
        .order_by(StocksTradingDetails.id.desc())

    rt = {}
    temp = []
    where = [StocksTradingDetails.id > 0]
    if searchVal:
        # 添加搜索关键词的模糊查询条件
        where.append(db.or_(StocksTradingDetails.code.like("%" + searchVal + "%"), StocksTradingDetails.name.like("%" + searchVal + "%")))

    if id:
        where.append(StocksTradingDetails.id == id)

    tc = db_tc.filter(*where).all()

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
        })

    rt['count'] = count
    rt['rows'] = temp

    return r(rt)


@route_api_stock.get('/newsList')
def newsList():
    """
    # 个股新闻
    :return:
    """
    searchVal = request.values.get('searchVal')
    userId = request.values.get('userId')

    # 获取监控stock
    selected_id = db.session.query(StocksSelected).filter_by(user_id=userId).all()
    selected_codes = {stock.code for stock in selected_id}

    where = [StocksNews.id > 0]
    if searchVal:
        # 添加搜索关键词的模糊查询条件
        where.append(db.or_(StocksNews.code.like("%" + searchVal + "%"), StocksNews.name.like("%" + searchVal + "%")))

    data = db.session.query(StocksNews).filter(*where).order_by(StocksNews.publish_time.desc()).all()
    filtered_data = [news for news in data if news.code in selected_codes]

    rt = {}
    temp = []
    # 返回json
    for t in filtered_data:
        temp.append({
            'code': t.code,
            'name': t.name,
            'title': t.title,
            'contents': t.contents,
            'publish_time': t.publish_time,
            'act_source': t.act_source,
            'url': t.url,
            'sentiment': t.sentiment
        })

    # 统计 sentiment 为 "消极" 的个数
    negative_num = 0
    for item in temp:
        if item.get('sentiment') == "消极":
            negative_num = negative_num + 1

    positive_num = 0
    for item in temp:
        if item.get('sentiment') == "积极":
            positive_num = positive_num + 1

    rt['rows'] = temp
    rt['count'] = len(temp)
    rt["negative_num"] = negative_num
    rt["negative_rate"] = str(round((negative_num / len(temp))*100,2)) + "%"
    rt["positive_num"] = positive_num
    rt["middle_num"] = len(temp) - (positive_num + negative_num)
    rt["sentiment"] = "消极" if negative_num > positive_num else "积极"

    # 舆情类型占比
    rt['sentiment_zb'] = [
        {'name': '积极', 'value': positive_num},
        {'name': '消极', 'value': negative_num},
        {'name': '中性', 'value': len(temp) - negative_num - positive_num},
    ]

    # # 日趋势折线图
    # 按日期和 sentiment 聚合数据
    aggregated_data = {}
    for item in temp:
        publish_date = item['publish_time'].date()
        sentiment = item['sentiment']
        if publish_date not in aggregated_data:
            aggregated_data[publish_date] = {}
        if sentiment not in aggregated_data[publish_date]:
            aggregated_data[publish_date][sentiment] = 0
        aggregated_data[publish_date][sentiment] += 1

    # 生成 ECharts 堆积折线图所需的 JSON 数据
    dates = sorted(aggregated_data.keys())
    sentiments = ['积极', '消极', '中性']
    series = []
    for sentiment in sentiments:
        data = []
        for date in dates:
            data.append(aggregated_data[date].get(sentiment, 0))
        series.append({
            'name': sentiment,
            'type': 'line',
            'smooth': 'true',
            'data': data
        })

    # 生成 ECharts 配置
    dateline = {
        'xAxis': {
            'type': 'category',
            "boundaryGap": "false",
            'data': [str(date) for date in dates]
        },
        'yAxis': {
        "type": 'value'
            },
        'series': series
    }

    # 将 ECharts 数据添加到返回结果中
    rt['dateline'] = dateline

    # 正面文章
    positive_data = [item for item in temp if item.get('sentiment') == "积极"]
    rt['positive_data'] = positive_data
    # 负面文章
    negative_data = [item for item in temp if item.get('sentiment') == "消极"]
    rt['negative_data'] = negative_data

    return r(rt)


@route_api_stock.get('/selection')
def selection():
    """
    # 查询自选
    :return:
    """
    userId = request.values.get('userId')

    data = db.session.query(StocksSelected.code, StocksSelected.name).filter_by(user_id=userId,is_news=1).all()
    re = []
    for x in data:
        re.append({'label': x[1], 'value': x[0]})
    return r({'options': re})
