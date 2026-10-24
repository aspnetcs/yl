# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/24 10:03

@mark    : 网格交易
"""
import pymysql
from applications.config import BaseConfig


def positive_t():
    """
    正T网格交易（下跌买入，上涨超过n%卖出）
    :return:
    """
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

            # 更新买卖价格
            update_price = """
                UPDATE stocks_trading_details a
                JOIN stocks b ON a.code = b.code
                JOIN stocks_selected c on a.selected_id = c.id
                SET a.next_price_buy = a.cjjg * (1 - a.zdf_tg) ,
                    a.next_price_sell = a.cjjg * (1 + a.zdf_tg),
                    a.zxj = b.zxj,
                    a.update_time = now()
                WHERE a.strategy_id = 8 -- 网格交易
                      AND a.is_monitor = 1 -- 是否监控
                """
            cursor.execute(update_price)
            connection.commit()

    finally:
        # 关闭数据库连接
        connection.close()
