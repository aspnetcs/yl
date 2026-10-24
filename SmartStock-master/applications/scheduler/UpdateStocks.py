# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 16:30

@mark    :
"""
import pymysql
import json
import datetime
from applications.config import BaseConfig
from applications.common.libs.tool import c_print
from applications.common.libs.stock.StockServer import get_stock_list, get_kline_detail, get_stock_list_HK, get_stocks_analyse, get_stocks_industry_fund_flow
from applications.common.libs.tool import is_within_work_hours



def update_stocks():
    """
    每天16:00更新股票列表到数据库表stocks
    :return:
    """
    # 获取当前时间
    now = datetime.datetime.now()

    # 检查是否在周一至周五的9:30到15:30之间
    if is_within_work_hours(now):
        c_print("开始更新股票列表stocks")
        try:

            # 获取股票列表
            json_list = get_stock_list()

            # 数据库连接配置
            db_config = {
                'host': BaseConfig.MYSQL_HOST,
                'user': BaseConfig.MYSQL_USERNAME,
                'password': BaseConfig.MYSQL_PASSWORD,
                'db': BaseConfig.MYSQL_DATABASE,
                'charset': 'utf8mb4',  # 确保支持Unicode字符
                'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式的游标
            }

            # 连接到数据库
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    # 遍历 JSON 列表，生成 SQL 更新语句
                    for item in json_list:
                        sql = f"""
                                    INSERT INTO stocks(region, code, name, zxj, zdf, zde, cjl, cje, syl_dt, sjl, zsz, ltsz, zdf_60d, zdf_nzj, update_time)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE
                                        name = VALUES(name),
                                        zxj = VALUES(zxj),
                                        zdf = VALUES(zdf),
                                        zde = VALUES(zde),
                                        cjl = VALUES(cjl),
                                        cje = VALUES(cje),
                                        syl_dt = VALUES(syl_dt),
                                        sjl = VALUES(sjl),
                                        zsz = VALUES(zsz),
                                        ltsz = VALUES(ltsz),
                                        zdf_60d = VALUES(zdf_60d),
                                        zdf_nzj = VALUES(zdf_nzj),
                                        update_time = VALUES(update_time)
                                """
                        # 提取字段值，注意顺序要与 SQL 中的占位符顺序一致
                        values = (
                            item['region'], item['stock_code'], item['stock_name'], item['zxj'], item['zdf'], item['zde'], item['cjl'], item['cje'],
                            item['syl_dt'], item['sjl'], item['zsz'], item['ltsz'], item['zdf_60d'], item['zdf_nzj'], item['update_time']
                        )
                        # 执行更新操作
                        cursor.execute(sql, values)

                    # 提交事务
                    connection.commit()
                    c_print("成功更新股票列表stocks")

            except Exception as e:
                # 捕获异常并回滚
                connection.rollback()
                c_print("更新股票列表stocks失败：", str(e))
                # 关闭数据库连接
                connection.close()

            finally:
                # 关闭连接
                connection.close()

        except Exception as e:
            c_print("更新股票列表stocks失败：", str(e))


def update_stocks_HK():
    """
    每天16:00更新股票列表到数据库表stocks
    :return:
    """
    # 获取当前时间
    now = datetime.datetime.now()

    # 检查是否在周一至周五的9:30到15:30之间
    if is_within_work_hours(now):
        c_print("开始更新股票列表stocks_HK")
        try:

            # 获取股票列表
            json_list = get_stock_list_HK()

            # 数据库连接配置
            db_config = {
                'host': BaseConfig.MYSQL_HOST,
                'user': BaseConfig.MYSQL_USERNAME,
                'password': BaseConfig.MYSQL_PASSWORD,
                'db': BaseConfig.MYSQL_DATABASE,
                'charset': 'utf8mb4',  # 确保支持Unicode字符
                'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式的游标
            }

            # 连接到数据库
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    # 遍历 JSON 列表，生成 SQL 更新语句
                    for item in json_list:
                        item['syl_dt'] = 0,
                        item['sjl'] = 0,
                        item['zsz'] = 0,
                        item['ltsz'] = 0,
                        item['zdf_60d'] = 0,
                        item['zdf_nzj'] = 0,
                        sql = f"""
                                    INSERT INTO stocks(region, code, name, zxj, zdf, zde, cjl, cje, syl_dt, sjl, zsz, ltsz, zdf_60d, zdf_nzj, update_time)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE
                                        name = VALUES(name),
                                        zxj = VALUES(zxj),
                                        zdf = VALUES(zdf),
                                        zde = VALUES(zde),
                                        cjl = VALUES(cjl),
                                        cje = VALUES(cje),
                                        syl_dt = VALUES(syl_dt),
                                        sjl = VALUES(sjl),
                                        zsz = VALUES(zsz),
                                        ltsz = VALUES(ltsz),
                                        zdf_60d = VALUES(zdf_60d),
                                        zdf_nzj = VALUES(zdf_nzj),
                                        update_time = VALUES(update_time)
                                """
                        # 提取字段值，注意顺序要与 SQL 中的占位符顺序一致
                        values = (
                            item['region'], item['stock_code'], item['stock_name'], item['zxj'], item['zdf'], item['zde'], item['cjl'], item['cje'],
                            item['syl_dt'], item['sjl'], item['zsz'], item['ltsz'], item['zdf_60d'], item['zdf_nzj'], item['update_time']
                        )
                        # 执行更新操作
                        cursor.execute(sql, values)

                    # 提交事务
                    connection.commit()
                    c_print("成功更新股票列表stocks")

            except Exception as e:
                # 捕获异常并回滚
                connection.rollback()
                c_print("更新股票列表stocks失败：", str(e))
                # 关闭数据库连接
                connection.close()

            finally:
                # 关闭连接
                connection.close()

        except Exception as e:
            c_print("更新股票列表stocks失败：", str(e))


def update_stocks_kline():
    """
    更新K线数据stocks_kline
    :return:
    """
    # 获取当前时间
    now = datetime.datetime.now()

    # 检查是否在周一至周五的9:30到15:30之间
    # if 1:
    if is_within_work_hours(now):
        c_print("开始更新股票k线数据stocks_kline")
        try:
            # 数据库连接配置
            db_config = {
                'host': BaseConfig.MYSQL_HOST,
                'user': BaseConfig.MYSQL_USERNAME,
                'password': BaseConfig.MYSQL_PASSWORD,
                'db': BaseConfig.MYSQL_DATABASE,
                'charset': 'utf8mb4',  # 确保支持Unicode字符
                'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式的游标
            }

            # 数据库查询自选股
            connection = pymysql.connect(**db_config)

            json_list = []
            try:
                # 更新指数K线
                codes_gb = [{"code": "000001", "name": "上证指数"},
                         {"code": "399001", "name": "深证成指"},
                         {"code": "399006", "name": "创业板指"},
                         {"code": "000300", "name": "沪深300"},
                         # {"code": "000905", "name": "中证500"},
                         # {"code": "000688", "name": "科创50"},
                         {"code": "HSI", "name": "恒生指数"},
                         {"code": "HSCEI", "name": "恒生国企指数"},
                         ]
                # 遍历指数列表，查询K线数据
                for code in codes_gb:
                    json_list_gb = get_kline_detail("GB", code['code'])
                    json_list.extend(json_list_gb)

            except Exception as e:
                c_print("查询指数K线失败：", str(e))


            # 更新股票列表
            try:
                with connection.cursor() as cursor:
                    # 遍历 JSON 列表，生成 SQL 更新语句
                    for item in json_list:
                        code = item['stock_code']
                        # 使用 INSERT ... ON DUPLICATE KEY UPDATE 实现 upsert 操作
                        # 假设表中已存在基于 (region, code, report_time) 的唯一索引
                        sql = """
                                                INSERT INTO stocks_kline (
                                                    region, code, name, zxj, cjl, cje, zg, zd, jk, report_time, update_time
                                                ) VALUES (
                                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                                )
                                                ON DUPLICATE KEY UPDATE
                                                    zxj = VALUES(zxj),
                                                    cjl = VALUES(cjl),
                                                    cje = VALUES(cje),
                                                    zg = VALUES(zg),
                                                    zd = VALUES(zd),
                                                    jk = VALUES(jk),
                                                    update_time = VALUES(update_time)
                                            """

                        # 提取字段值
                        values = (
                            item['region'],  # region
                            code,  # code
                            item['stock_name'],  # name
                            item['zxj'],  # 最新价
                            item['cjl'],  # 成交量
                            item['cje'],  # 成交额
                            item['zg'],  # 最高价
                            item['zd'],  # 最低价
                            item['jk'],  # 收盘价
                            item['report_time'],  # report_time
                            item['update_time']  # update_time
                        )

                        # 执行 upsert 操作
                        cursor.execute(sql, values)

                    # 提交事务
                    connection.commit()
                    c_print("成功更新股票k线stocks_kline")

            except Exception as e:
                # 捕获异常并回滚
                connection.rollback()
                c_print("更新股票k线stocks_kline失败：", str(e))
                # 关闭数据库连接
                connection.close()

            finally:
                # 关闭连接
                connection.close()

        except Exception as e:
            c_print("更新股票k线stocks_kline失败：", str(e))


def update_stocks_analyse():
    """
    更新股票分析详情
    :return:
    """
    try:
        c_print("开始更新股票分析stocks_analyse")
        # 获取股票分析宽表
        json_list = get_stocks_analyse()

        # 数据库连接配置
        db_config = {
            'host': BaseConfig.MYSQL_HOST,
            'user': BaseConfig.MYSQL_USERNAME,
            'password': BaseConfig.MYSQL_PASSWORD,
            'db': BaseConfig.MYSQL_DATABASE,
            'charset': 'utf8mb4',  # 确保支持Unicode字符
            'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式的游标
        }

        # 连接到数据库
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                for item in json_list:
                    code = item['stock_code']
                    # 使用 INSERT ... ON DUPLICATE KEY UPDATE 实现 upsert 操作
                    # 假设表中已存在基于 (region, code, report_time) 的唯一索引
                    sql = """
                                INSERT INTO stocks_analyse (
                                    region,code,name,zsz,ltsz,syl_dt,sjl,zxj,zdf_60d,zdf_nzj,mgsy,yysr_yysr
                                    ,yysr_tbzz,yysr_jdhbzz,jlr_jlr,jlr_tbzz,jlr_jdhbzz,mgjzc,jzcsyl,mgjyxjll,xsmll,schy,report_date,update_time
                                ) VALUES (
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                )
                                ON DUPLICATE KEY UPDATE
                                    zsz = VALUES(zsz),
                                    ltsz = VALUES(ltsz),
                                    zdf_60d = VALUES(zdf_60d),
                                    zdf_nzj = VALUES(zdf_nzj),
                                    mgsy = VALUES(mgsy),
                                    yysr_yysr = VALUES(yysr_yysr),
                                    yysr_tbzz = VALUES(yysr_tbzz),
                                    yysr_jdhbzz = VALUES(yysr_jdhbzz),
                                    jlr_jlr = VALUES(jlr_jlr),
                                    jlr_tbzz = VALUES(jlr_tbzz),
                                    jlr_jdhbzz = VALUES(jlr_jdhbzz),
                                    mgjzc = VALUES(mgjzc),
                                    jzcsyl = VALUES(jzcsyl),
                                    mgjyxjll = VALUES(mgjyxjll),
                                    xsmll = VALUES(xsmll),
                                    schy = VALUES(schy),
                                    report_date = VALUES(report_date),
                                    update_time = VALUES(update_time)
                                        """
                    # 提取字段值
                    values = (
                        item['region'],  # region
                        code,  # code
                        item['stock_name'],  # name
                        item['zsz'],  # 总市值
                        item['ltsz'],  # 流通市值
                        item['syl_dt'],  # 市盈率（动态）
                        item['sjl'],  # 市净率
                        item['zxj'],  # 最新价
                        item['zdf_60d'],  # 60天涨跌幅
                        item['zdf_nzj'],  # 最近涨跌幅
                        item['mgsy'],  # 流通市值
                        item['yysr_yysr'],  # 昨日收益
                        item['yysr_tbzz'],  # 昨日收益（同比）
                        item['yysr_jdhbzz'],  # 昨日收益（季度环比）
                        item['jlr_jlr'],  # 今日量比
                        item['jlr_tbzz'],  # 今日量比（同比）
                        item['jlr_jdhbzz'],  # 今日量比（季度环比）
                        item['mgjzc'],  # 流通市值
                        item['jzcsyl'],  # 流通市值（同比）
                        item['mgjyxjll'],  # 流通市值（同比）
                        item['xsmll'],  # 流通市值（同比）
                        item['schy'],  # 流通市值（同比）
                        item['report_date'],  # report_date
                        item['update_time']  # update_time
                    )
                    # 执行SQL语句
                    cursor.execute(sql, values)

                # 提交事务
                connection.commit()

                c_print("更新股票分析stocks_analyse成功")

        except Exception as e:
            connection.rollback()  # 回滚事务
            c_print("更新股票分析stocks_analyse失败：", str(e))

    except Exception as e:
        c_print("更新股票分析stocks_analyse失败：", str(e))

    finally:
        # 关闭数据库连接
        connection.close()



def update_industry_fund_flow():
    """
    更新行业资金流向报表
    :return:
    """
    c_print(f"开始更新行业资金流向stocks_industry_fund_flow")
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        # 获取股票列表
        json_list = get_stocks_industry_fund_flow(date)

        # 数据库连接配置
        db_config = {
            'host': BaseConfig.MYSQL_HOST,
            'user': BaseConfig.MYSQL_USERNAME,
            'password': BaseConfig.MYSQL_PASSWORD,
            'db': BaseConfig.MYSQL_DATABASE,
            'charset': 'utf8mb4',  # 确保支持Unicode字符
            'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式的游标
        }

        # 连接到数据库
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:

                # 删除旧数据
                delete_query = f"DELETE FROM stocks_industry_fund_flow WHERE report_date = '{date}'"
                cursor.execute(delete_query)
                # 提交事务
                connection.commit()

                # 表结构与JSON中的键匹配
                insert_sql = """
                INSERT INTO stocks_industry_fund_flow (code, name, zxj, zdf, zsz, hsl, report_date, update_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                # 遍历JSON列表并执行插入操作
                for record in json_list:
                    # 注意：这里需要确保record中的键与insert_sql中的占位符顺序一致
                    # 或者你可以使用命名参数（如果数据库驱动支持）来避免顺序问题
                    # 提取字段值
                    values = (
                        record['code'],
                        record['name'],
                        record['zxj'],
                        record['zdf'],
                        record['zsz'],
                        record['hsl'],
                        record['report_date'],
                        record['update_time']
                    )
                    # 执行SQL语句
                    cursor.execute(insert_sql, values)

                # 提交事务
                connection.commit()

                c_print("成功更新行业资金流向stocks_industry_fund_flow")

        except Exception as e:
            c_print("更新行业资金流向stocks_industry_fund_flow失败：", str(e))
            # 关闭数据库连接
            connection.close()

    except Exception as e:
        c_print("更新行业资金流向stocks_industry_fund_flow失败：", str(e))



if __name__ == "__main__":

    update_stocks()
    # update_stocks_HK()
    # update_stocks_kline()
    # update_stocks_analyse()
    # update_industry_fund_flow()
