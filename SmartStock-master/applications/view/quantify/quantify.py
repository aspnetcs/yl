# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 13:34

@mark    :
"""
import datetime
from sqlalchemy import func
from sqlalchemy import and_
from flask import Blueprint, render_template, request, json
from flask_login import current_user
from applications.models.stock.StocksQuantify import StocksQuantify
from applications.models.stock.StocksAnalyse import StocksAnalyse
from applications.models.stock.StocksSelected import StocksSelected
from applications.extensions import db
from applications.common.libs.jsonformat import r

route_quantify = Blueprint('selection', __name__, url_prefix='/selection')


@route_quantify.get('/')
def main():
    update_time = db.session.query(func.max(StocksAnalyse.update_time)).scalar()

    return render_template('quantify/selection/main.html', updateTime=update_time)


@route_quantify.get('/list')
def quantify_list():
    """
    获取行情列表
    :return:
    """
    def str_to_int(num):
        """
        字符串转数字
        :param num:
        :return:
        """
        if num is None:
            return None
        elif num == '':
            return None
        else:
            return float(num)

    # 接收参数
    pageSize = str_to_int(request.values.get('pageSize'))
    pageNo = str_to_int(request.values.get('pageNo'))
    name = request.values.get('name')
    schy = request.values.get('schy')
    zszMin = str_to_int(request.values.get('zszMin'))
    zszMax = str_to_int(request.values.get('zszMax'))
    sylMin = str_to_int(request.values.get('sylMin'))
    sylMax = str_to_int(request.values.get('sylMax'))
    sjlMin = str_to_int(request.values.get('sjlMin'))
    sjlMax = str_to_int(request.values.get('sjlMax'))
    zxjMin = str_to_int(request.values.get('zxjMin'))
    zxjMax = str_to_int(request.values.get('zxjMax'))
    mgsyMin = str_to_int(request.values.get('mgsyMin'))
    mgsyMax = str_to_int(request.values.get('mgsyMax'))
    yysrMin = str_to_int(request.values.get('yysrMin'))
    yysrMax = str_to_int(request.values.get('yysrMax'))
    yysr_tbzzMin = str_to_int(request.values.get('yysr_tbzzMin'))
    yysr_tbzzMax = str_to_int(request.values.get('yysr_tbzzMax'))
    jlrMin = str_to_int(request.values.get('jlrMin'))
    jlrMax = str_to_int(request.values.get('jlrMax'))
    jlr_tbzzMin = str_to_int(request.values.get('jlr_tbzzMin'))
    jlr_tbzzMax = str_to_int(request.values.get('jlr_tbzzMax'))
    mgjzcMin = str_to_int(request.values.get('mgjzcMin'))
    mgjzcMax = str_to_int(request.values.get('mgjzcMax'))
    jzcsylMin = str_to_int(request.values.get('jzcsylMin'))
    jzcsylMax = str_to_int(request.values.get('jzcsylMax'))

    # 数据库响应
    sel_tc = db.session.query(StocksSelected.code).filter_by(user_id=current_user.id).all()
    stock_codes = [code[0] for code in sel_tc]
    # print(stock_codes)
    db_tc = db.session.query(StocksAnalyse).order_by(StocksAnalyse.zxj.desc())

    if pageNo is None:
        pageNo = 1
        pageSize = 10
        offset = ((pageNo - 1) * pageSize)
    else:
        offset = (pageNo - 1) * pageSize

    rt = {}
    temp = []
    where = [and_(StocksAnalyse.zsz > 0, StocksAnalyse.yysr_yysr > 0,StocksAnalyse.ltsz > 0,StocksAnalyse.zxj > 0)]
    if name:
        where.append(StocksAnalyse.name.like("%" + name + "%"))
    if schy:
        where.append(StocksAnalyse.schy.like("%" + schy + "%"))

    if zszMin:
        where.append(StocksAnalyse.zsz >= zszMin)
    if zszMax:
        where.append(StocksAnalyse.zsz <= zszMax)

    if sylMin:
        where.append(StocksAnalyse.syl_dt >= sylMin)
    if sylMax:
        where.append(StocksAnalyse.syl_dt <= sylMax)

    if sjlMin:
        where.append(StocksAnalyse.sjl >= sjlMin)
    if sjlMax:
        where.append(StocksAnalyse.sjl <= sjlMax)

    if zxjMin:
        where.append(StocksAnalyse.zxj >= zxjMin)
    if zxjMax:
        where.append(StocksAnalyse.zxj <= zxjMax)

    if mgsyMin:
        where.append(StocksAnalyse.mgsy >= mgsyMin)
    if mgsyMax:
        where.append(StocksAnalyse.mgsy <= mgsyMax)

    if yysrMin:
        where.append(StocksAnalyse.yysr_yysr >= yysrMin * 100000000)
    if yysrMax:
        where.append(StocksAnalyse.yysr_yysr <= yysrMax * 100000000)

    if yysr_tbzzMin:
        where.append(StocksAnalyse.yysr_tbzz >= yysr_tbzzMin)
    if yysr_tbzzMax:
        where.append(StocksAnalyse.yysr_tbzz <= yysr_tbzzMax)

    if jlrMin:
        where.append(StocksAnalyse.jlr_jlr >= jlrMin * 100000000)
    if jlrMax:
        where.append(StocksAnalyse.jlr_jlr <= jlrMax * 100000000)

    if jlr_tbzzMin:
        where.append(StocksAnalyse.jlr_tbzz >= jlr_tbzzMin)
    if jlr_tbzzMax:
        where.append(StocksAnalyse.jlr_tbzz <= jlr_tbzzMax)

    if mgjzcMin:
        where.append(StocksAnalyse.mgjzc >= mgjzcMin)
    if mgjzcMax:
        where.append(StocksAnalyse.mgjzc <= mgjzcMax)

    if jzcsylMin:
        where.append(StocksAnalyse.jzcsyl >= jzcsylMin)
    if jzcsylMax:
        where.append(StocksAnalyse.jzcsyl <= jzcsylMax)

    # 表格
    tc = db_tc.filter(*where).limit(pageSize).offset(offset).all()
    count = db_tc.filter(*where).count()

    # 行业分布
    df_hy = db.session.query(StocksAnalyse.schy.label('schy'),
                            func.count(1).label('count')).filter(*where).group_by('schy').all()

    # 转换结果到所需的格式
    df_hy_rt = [{'name': schy, 'value': count} for schy, count in df_hy]

    # 个股市值TOP10排序
    df_zsz = db.session.query(StocksAnalyse.name, StocksAnalyse.zsz).filter(*where).order_by(StocksAnalyse.zsz.desc()).limit(10).all()
    # 转换结果到柱状图所需的格式
    name = [item[0] for item in df_zsz]
    zsz = [round(item[1], 1) for item in df_zsz]
    df_zsz_rt = {'name': name, 'zsz': zsz}

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
            'zxj': t.zxj,
            'syl_dt': t.syl_dt,
            'sjl': t.sjl,
            'zsz': round(t.zsz, 1),
            'ltsz': str(round(t.ltsz, 2)) + '亿' if t.ltsz is not None else None,
            'zdf_60d': str(round(t.zdf_60d, 2)) + '%' if t.zdf_60d is not None else None,
            'zdf_nzj': str(round(t.zdf_nzj, 2)) + '%' if t.zdf_nzj is not None else None,
            'mgsy': t.mgsy,
            'yysr_yysr': round(t.yysr_yysr / 100000000, 1),
            'yysr_tbzz': str(round(t.yysr_tbzz, 2)) + '%' if t.yysr_tbzz is not None else None,
            'yysr_jdhbzz': t.yysr_jdhbzz,
            'jlr_jlr': round(t.jlr_jlr / 100000000, 1),
            'jlr_tbzz': str(round(t.jlr_tbzz, 2)) + '%' if t.jlr_tbzz is not None else None,
            'jlr_jdhbzz': t.jlr_jdhbzz,
            'mgjzc': round(t.mgjzc, 2),
            'jzcsyl': t.jzcsyl,
            'mgjyxjll': round(t.mgjyxjll, 2),
            'xsmll': str(round(t.xsmll, 2)) + '%' if t.xsmll is not None else None,
            'schy': t.schy,
            'report_date': t.report_date,
            'update_time': t.update_time,
            'is_selected': is_selected
        })

    rt['count'] = count
    rt['rows'] = temp
    rt['hy'] = df_hy_rt
    rt['zsz'] = df_zsz_rt

    return r(rt)


@route_quantify.route('/add')
def add():
    """
    # 添加自选
    :return:
    """
    return render_template('quantify/selection/add.html')


@route_quantify.route('/filterSave', methods=['POST'])
def filterSave():
    """
    # 保存条件
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)
    # print(j_data)

    fit = db.session.query(StocksQuantify).filter_by(name=j_data['name'], user_id=current_user.id).first()

    if fit is not None:
        return r({}, 0, '', '条件已存在')

    tc = StocksQuantify(
        user_id=current_user.id,
        name=j_data['name'],
        filter=j_data['filter'],
        mark=j_data['mark'],
        update_time=str(datetime.datetime.now())
    )
    db.session.add(tc)
    db.session.commit()

    return r({}, 0, '添加成功')



@route_quantify.route('/del', methods=['GET'])
def delProject():
    """
    # 删除自选
    :return:
    """
    selectedCode = request.values.get('code')
    db.session.query(StocksSelected).filter_by(code=selectedCode, user_id=current_user.id).delete()
    db.session.commit()
    return r({}, 0, '删除成功')


@route_quantify.route('/edit')
def edit():
    """
    # 添加自选
    :return:
    """
    return render_template('quantify/selection/edit.html')


@route_quantify.route('/editSave', methods=['POST'])
def editSave():
    """
    # 保存条件
    :return:
    """
    data = request.get_data()
    j_data = json.loads(data)
    # print(j_data)

    fit = db.session.query(StocksQuantify).filter_by(name=j_data['name'], user_id=current_user.id).filter(
        StocksQuantify.id != j_data['id']).first()

    if fit is not None:
        return r({}, 0, '', '条件已存在')

    tc = db.session.query(StocksQuantify).filter_by(id=j_data['id']).first()

    tc.name = j_data['name'],
    tc.filter = j_data['filter'],
    tc.mark = j_data['mark'],
    tc.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

    db.session.commit()

    return r({}, 0, '修改成功')