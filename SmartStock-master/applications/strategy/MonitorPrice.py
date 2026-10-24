# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/4/11 13:09

@mark    :  监控到价
"""
import pymysql
from applications.config import BaseConfig


def monitorPrice():
    """
    监控到价策略：到价买入10000元
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
            # 设置锁超时和隔离级别
            cursor.execute("SET SESSION innodb_lock_wait_timeout = 5")
            cursor.execute("SET SESSION transaction_isolation = 'READ-COMMITTED'")

            # 开始事务
            connection.begin()

            # 先查询需要更新的记录ID
            select_query = """
            SELECT a.id 
            FROM stocks_strategy_details a
            JOIN stocks b ON a.code = b.code
            JOIN stocks_selected c ON a.selected_id = c.id
            WHERE a.strategy_id = 9
            """
            cursor.execute(select_query)
            record_ids = [row['id'] for row in cursor.fetchall()]

            if not record_ids:
                connection.commit()
                return

            # 分批更新，每批50条记录
            batch_size = 50
            for i in range(0, len(record_ids), batch_size):
                batch_ids = record_ids[i:i + batch_size]
                id_list = ','.join(str(id) for id in batch_ids)

                update_zxj = f"""
                UPDATE stocks_strategy_details a
                JOIN stocks b ON a.code = b.code
                JOIN stocks_selected c ON a.selected_id = c.id
                SET a.zxj = b.zxj,
                    a.total_invest_budget = c.total_invest_budget,
                    a.income_rate_target = c.income_rate_target,
                    a.income_target = c.total_invest_budget * c.income_rate_target,
                    a.next_price_buy = a.view_price,
                    a.next_price_sell = a.view_price*(1+a.income_rate_target),
                    a.total_invested = c.cost_price*c.hold_number,
                    a.suggest_buy_amt = (ROUND((c.total_invest_budget*a.add_fund)/(b.zxj * 100)) * 100) * b.zxj,
                    a.suggest_buy_num = ROUND((c.total_invest_budget*a.add_fund)/(b.zxj * 100)) * 100,
                    a.update_time = now()
                WHERE a.id IN ({id_list})
                AND a.strategy_id = 9
                """
                cursor.execute(update_zxj)

            # 提交事务
            connection.commit()

    except pymysql.err.OperationalError as e:
        # 处理死锁和锁超时异常
        if e.args[0] in [1213, 1205]:  # 死锁和锁超时错误代码
            print("检测到数据库锁问题，正在回滚事务...")
            connection.rollback()
            print("事务已回滚，稍后重试")
        else:
            connection.rollback()
            print(f"数据库操作错误: {str(e)}")
    except Exception as e:
        connection.rollback()
        print(f"更新监控到价策略失败：{str(e)}")
    finally:
        # 关闭数据库连接
        connection.close()
