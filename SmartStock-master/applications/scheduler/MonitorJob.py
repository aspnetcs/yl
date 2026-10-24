# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/7 16:24

@mark    :
"""
import pymysql
from applications.config import BaseConfig
from applications.common.libs.tool import c_print
from applications.strategy.GridTrading import positive_t


def monitor_msg_data():
    """
    # 获取消息队列数据
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

            # 消息队列
            monitor_query = f"""
            select strategy_details_id,
                    strategy_type,
                    code,
                    name,
                    zxj,
                    next_price_buy,
                    suggest_buy_num,
                    suggest_buy_amt,
                    strategy_id,
                    strategy_name,
                    cost_price,
                    hold_number,
                    income_rate,
                    hold_amt_after,
                    hold_num_after,
                    price_after,
                    income_rate_after,
                    suggest_sale_num,
                    suggest_sale_amt,
                    income_amt,
                    user_id,
                    is_send,
                    msg_type,
                    create_time,
                    update_time
                    ,b.email
                    ,b.email_passwd
                    ,ding_access_token
                    ,ding_secret
                    ,b.monitor_type
                    from stock_msg_queue a 
                    inner join admin_user b on a.user_id = b.id
                    where create_time >= CURDATE() 
                    and is_send = 0
            """
            cursor.execute(monitor_query)

            result = cursor.fetchall()

            return result

    except Exception as e:
        c_print("触发买入预警失败：", str(e))
        # 关闭数据库连接
        connection.close()



if __name__ == "__main__":
    data = monitor_msg_data()
    print(data)
