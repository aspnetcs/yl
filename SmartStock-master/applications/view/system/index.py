# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2024/1/5 13:14

@mark    : 首页视图
"""
import datetime
import json
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from applications.common.libs.tool import filter_by_json, coalesce
from applications.common.libs.jsonformat import r
from applications.extensions import db
from applications.models.stock.StocksNews import StocksNews
from applications.models.stock.StocksSelected import StocksSelected
from applications.config import BaseConfig
from applications.models.stock.StocksKline import StocksKline
from applications.models.stock.StocksIndustryFundFlow import StocksIndustryFundFlow


bp = Blueprint('index', __name__, url_prefix='/')


@bp.get('/')
@login_required
def index():
    """
    # 首页
    :return:
    """
    user = current_user
    return render_template('system/index.html', user=user, sys_name=BaseConfig.SYSTEM_NAME)


@bp.route('/home/target')
def get_data():
    """
    # 指标卡
    :return:
    """
    rt = {}

    # 获取所有需要处理的股票代码
    target_codes = ["000001", "399001", "399006", "000300", "HSI", "HSCEI"]

    # 为每个股票代码获取最近两个交易日的记录
    kline_data = {}
    for code in target_codes:
        # 获取该股票代码的最近两个记录
        last_two_records = StocksKline.query.filter(
            StocksKline.region == "GB",
            StocksKline.code == code
        ).order_by(StocksKline.report_time.desc()).limit(2).all()
        # print(last_two_records)
        if len(last_two_records) >= 2:
            kline_data[code] = last_two_records

    # 上证指数
    if "000001" in kline_data and len(kline_data["000001"]) >= 2:
        sz_zs = kline_data["000001"]
        rt['sz_zs'] = coalesce(sz_zs[0].zxj, 0)
        rt['sz_zdf'] = round(coalesce((sz_zs[0].zxj - sz_zs[1].zxj)/sz_zs[1].zxj, 0) * 100, 2)
        if rt['sz_zdf'] > 0:
            rt['sz_color'] = "red"
        elif rt['sz_zdf'] < 0:
            rt['sz_color'] = "green"
        else:
            rt['sz_color'] = "gray"
    else:
        rt['sz_zs'] = 0
        rt['sz_zdf'] = 0
        rt['sz_color'] = "gray"

    # 深证成指
    if "399001" in kline_data and len(kline_data["399001"]) >= 2:
        sc_zs = kline_data["399001"]
        rt['sc_zs'] = coalesce(sc_zs[0].zxj, 0)
        rt['sc_zdf'] = round(coalesce((sc_zs[0].zxj - sc_zs[1].zxj)/sc_zs[1].zxj, 0) * 100, 2)
        if rt['sc_zdf'] > 0:
            rt['sc_color'] = "red"
        elif rt['sc_zdf'] < 0:
            rt['sc_color'] = "green"
        else:
            rt['sc_color'] = "gray"
    else:
        rt['sc_zs'] = 0
        rt['sc_zdf'] = 0
        rt['sc_color'] = "gray"

    # 创业版指
    if "399006" in kline_data and len(kline_data["399006"]) >= 2:
        cyb_zs = kline_data["399006"]
        rt['cyb_zs'] = coalesce(cyb_zs[0].zxj, 0)
        rt['cyb_zdf'] = round(coalesce((cyb_zs[0].zxj - cyb_zs[1].zxj)/cyb_zs[1].zxj, 0) * 100, 2)
        if rt['cyb_zdf'] > 0:
            rt['cyb_color'] = "red"
        elif rt['cyb_zdf'] < 0:
            rt['cyb_color'] = "green"
        else:
            rt['cyb_color'] = "gray"
    else:
        rt['cyb_zs'] = 0
        rt['cyb_zdf'] = 0
        rt['cyb_color'] = "gray"

    # 沪深300
    if "000300" in kline_data and len(kline_data["000300"]) >= 2:
        hs300_zs = kline_data["000300"]
        rt['hs300_zs'] = coalesce(hs300_zs[0].zxj, 0)
        rt['hs300_zdf'] = round(coalesce((hs300_zs[0].zxj - hs300_zs[1].zxj)/hs300_zs[1].zxj, 0) * 100, 2)
        if rt['hs300_zdf'] > 0:
            rt['hs300_color'] = "red"
        elif rt['hs300_zdf'] < 0:
            rt['hs300_color'] = "green"
        else:
            rt['hs300_color'] = "gray"
    else:
        rt['hs300_zs'] = 0
        rt['hs300_zdf'] = 0
        rt['hs300_color'] = "gray"

    # 恒生指数
    if "HSI" in kline_data and len(kline_data["HSI"]) >= 2:
        hsi_zs = kline_data["HSI"]
        rt['hsi_zs'] = coalesce(hsi_zs[0].zxj, 0)
        rt['hsi_zdf'] = round(coalesce((hsi_zs[0].zxj - hsi_zs[1].zxj)/hsi_zs[1].zxj, 0) * 100, 2)
        if rt['hsi_zdf'] > 0:
            rt['hsi_color'] = "red"
        elif rt['hsi_zdf'] < 0:
            rt['hsi_color'] = "green"
        else:
            rt['hsi_color'] = "gray"
    else:
        rt['hsi_zs'] = 0
        rt['hsi_zdf'] = 0
        rt['hsi_color'] = "gray"

    # 国企指数
    if "HSCEI" in kline_data and len(kline_data["HSCEI"]) >= 2:
        hscei_zs = kline_data["HSCEI"]
        rt['hscei_zs'] = coalesce(hscei_zs[0].zxj, 0)
        rt['hscei_zdf'] = round(coalesce((hscei_zs[0].zxj - hscei_zs[1].zxj)/hscei_zs[1].zxj, 0) * 100, 2)
        if rt['hscei_zdf'] > 0:
            rt['hscei_color'] = "red"
        elif rt['hscei_zdf'] < 0:
            rt['hscei_color'] = "green"
        else:
            rt['hscei_color'] = "gray"
    else:
        rt['hscei_zs'] = 0
        rt['hscei_zdf'] = 0
        rt['hscei_color'] = "gray"

    return r(rt)


@bp.route('/home/szZs')
def szZs():
    """
    # 上证指数K线图
    :return:
    """
    data = StocksKline.query.filter(
        StocksKline.region == "GB",
        StocksKline.code == "000001"
    ).order_by(StocksKline.report_time.asc()).limit(365).all()

    new_data = []

    # 遍历给定的列表
    for item in data:
        new_row = [item.report_time.strftime('%Y-%m-%d'), float(item.jk), float(item.zxj), float(item.zd), float(item.zg)]
        new_data.append(new_row)

    json_data = {
        "status": 0,
        "msg": "ok",
        "data": new_data
    }

    json_str = json.dumps(json_data)

    return json_str



@bp.route('/home/szCz')
def szCz():
    """
    # 深证成指K线图
    :return:
    """
    data = StocksKline.query.filter(
        StocksKline.region == "GB",
        StocksKline.code == "399001"
    ).order_by(StocksKline.report_time.asc()).limit(365).all()

    new_data = []

    # 遍历给定的列表
    for item in data:
        new_row = [item.report_time.strftime('%Y-%m-%d'), float(item.jk), float(item.zxj), float(item.zd), float(item.zg)]
        new_data.append(new_row)

    json_data = {
        "status": 0,
        "msg": "ok",
        "data": new_data
    }

    json_str = json.dumps(json_data)

    return json_str


@bp.route('/home/hyBk')
def hyBk():
    """
    # 行业板块
    :return:
    """
    max_date = db.session.query(db.func.max(StocksIndustryFundFlow.report_date)).scalar()

    data = StocksIndustryFundFlow.query.filter(
        StocksIndustryFundFlow.report_date == max_date
    ).order_by(StocksIndustryFundFlow.zdf.desc()).limit(6).all()

    # sorted_data = sorted(data, key=lambda x: x['zdf'], reverse=True)[:6]

    name = [item.name for item in data]
    rqs = [item.zdf for item in data]
    rqs_pc = [str(item.zdf) + '%' for item in data]

    json_data = {
        "status": 0,
        "msg": "ok",
        "data": {
            "name": name,
            "rqs": rqs,
            "rqs_pc": rqs_pc
        }
    }

    json_str = json.dumps(json_data)

    return json_str


@bp.route('/home/globalNews')
def globalNews():
    """
    # 财经快讯
    :return:
    """
    data = db.session.query(StocksNews).filter_by(code=0).all()

    rt = {}
    temp = []
    # 返回json
    for t in data:
        temp.append({
            'code': t.code,
            'title': t.title,
            'contents': t.contents,
            'publish_time': t.publish_time,
            'act_source': t.act_source,
            'url': t.url,
            'is_hot': t.is_hot
        })

    rt['rows'] = temp

    return r(rt)


@bp.route('/home/stocksNews')
def stocksNews():
    """
    # 个股新闻
    :return:
    """
    # 获取监控stock
    selected_id = db.session.query(StocksSelected).filter_by(is_news=1, user_id=current_user.id).all()
    selected_codes = {stock.code for stock in selected_id}

    data = db.session.query(StocksNews).filter_by(is_hot=1).all()
    filtered_data = [news for news in data if news.code in selected_codes]

    rt = {}
    temp = []
    # 返回json
    for t in filtered_data:
        temp.append({
            'code': t.code,
            'title': t.title,
            'contents': t.contents,
            'publish_time': t.publish_time,
            'act_source': t.act_source,
            'url': t.url
        })

    rt['rows'] = temp

    return r(rt)

