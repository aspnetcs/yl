# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/25 16:58

@mark    :
"""
import datetime
from sqlalchemy import func
from flask import Blueprint, render_template, request, json
from flask_login import current_user
from sqlalchemy import or_
from applications.models import StocksNews
from applications.models.stock.Stocks import Stocks
from applications.models.stock.StocksSelected import StocksSelected
from applications.extensions import db
from applications.common.libs.jsonformat import r

route_news = Blueprint('news', __name__, url_prefix='/news')


@route_news.get('/')
def main():

    return render_template('stock/news/main.html')


@route_news.get('/list')
def news_list():
    """
    # 个股新闻
    :return:
    """
    code = request.values.get('code')
    name = request.values.get('name')

    # 获取监控stock
    selected_id = db.session.query(StocksSelected).filter_by(user_id=current_user.id).all()
    selected_codes = {stock.code for stock in selected_id}

    where = [StocksNews.id > 0]
    if code:
        where.append(StocksNews.code.like("%" + code + "%"))
    if name:
        where.append(StocksNews.name.like("%" + name + "%"))


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
    rt["negative_rate"] = "0%" if len(temp) == 0 else str(round((negative_num / len(temp))*100,2)) + "%"
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


@route_news.get('/selection')
def selection():
    """
    # 查询自选
    :return:
    """
    data = db.session.query(StocksSelected.code, StocksSelected.name).filter_by(user_id=current_user.id,is_news=1).all()
    re = []
    for x in data:
        re.append({'label': x[1], 'value': x[0]})
    return r({'options': re})

