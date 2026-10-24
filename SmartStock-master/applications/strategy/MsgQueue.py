# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/6 16:24

@mark    : 推送消息队列
"""
import pymysql
from applications.config import BaseConfig


def msg_queue():
    """
    推送消息队列
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

            # 更新最新价
            update_data = """
                        -- 个股买入消息
                        select a.id as strategy_details_id
                              ,0 as strategy_type
                              ,a.`code`  -- 编码
                              ,a.`name`  -- 名称
                              ,a.zxj  -- 最新价
                              ,a.next_price_buy  -- 下一买点
                              ,round(a.suggest_buy_num,0) as suggest_buy_num  -- 建议购买数量
                              ,round(a.suggest_buy_amt,0) as suggest_buy_amt  -- 建议购买金额
                              ,a.strategy_id
                              ,d.name as strategy_name  -- 策略名
                              ,c.cost_price -- 当前持仓价格
                              ,round(hold_number,0) as hold_number -- 当前持仓数量
                              ,concat(round(((a.zxj-c.cost_price)/c.cost_price)*100,2),'%') as income_rate -- 当前收益率
                              ,round(suggest_buy_amt + cost_price*hold_number,0) as hold_amt_after -- 买入后持仓金额
                              ,round(hold_number + suggest_buy_num,0) as hold_num_after -- 买入后持仓数量
                              ,round((suggest_buy_amt + cost_price*hold_number)/(hold_number + suggest_buy_num),2) as price_after -- 买入后持仓价格
                              ,concat(round((((hold_number + suggest_buy_num)*zxj - (suggest_buy_amt + cost_price*hold_number))/(suggest_buy_amt + cost_price*hold_number))*100,2),'%') as income_rate_after-- 买入后收益率
                              ,null as suggest_sale_num -- 建议卖出数量
                              ,null as suggest_sale_amt -- 建议卖出金额
                              ,null as income_amt -- 收入金额
                              ,a.user_id  
                              ,0 as is_send
                              ,0 as msg_type
                              ,NOW() as create_time
                              ,NOW() as update_time
                        from stocks_strategy_details a 
                        inner join stocks_selected c on a.selected_id = c.id
                        inner join stocks_strategy d on a.strategy_id = d.id
                        where is_monitor = 1
                        and zxj <= next_price_buy -- 当前价格低于下次价格
                        and c.total_invest_budget >= c.cost_price * hold_number
                        
                        union all 
                        
                        -- 单笔交易买入消息
                        select a.id as trading_details_id
                              ,1 as strategy_type
                              ,a.`code`  -- 编码
                              ,a.`name`  -- 名称
                              ,a.zxj  -- 最新价
                              ,a.next_price_buy  -- 下一买点
                              ,cjsl as suggest_buy_num  -- 建议购买数量
                              ,a.zxj * cjsl as suggest_buy_amt  -- 建议购买金额
                              ,a.strategy_id
                              ,d.name as strategy_name  -- 策略名
                              ,c.cost_price -- 当前持仓价格
                              ,round(hold_number,0) as hold_number -- 当前持仓数量
                              ,concat(round(((a.zxj-c.cost_price)/c.cost_price)*100,2),'%') as income_rate -- 当前收益率
                              ,round(a.zxj * cjsl + cost_price*hold_number,0) as hold_amt_after -- 买入后持仓金额
                              ,round(hold_number + cjsl,0) as hold_num_after -- 买入后持仓数量
                              ,round((a.zxj * cjsl + cost_price*hold_number)/(hold_number + cjsl),2) as price_after -- 买入后持仓价格
                              ,concat(round((((hold_number + cjsl)*zxj - (a.zxj * cjsl + cost_price*hold_number))/(a.zxj * cjsl + cost_price*hold_number))*100,2),'%') as income_rate_after-- 买入后收益率
                              ,null as suggest_sale_num -- 建议卖出数量
                              ,null as suggest_sale_amt -- 建议卖出金额
                              ,null as income_amt -- 收入金额
                              ,a.user_id 
                              ,0 as is_send
                              ,0 as msg_type
                              ,NOW() as create_time
                              ,NOW() as update_time
                        from stocks_trading_details a 
                        inner join stocks_selected c on a.selected_id = c.id
                        inner join stocks_strategy d on a.strategy_id = d.id
                        where is_monitor = 1 
                        and zxj <= next_price_buy -- 当前价格低于下次价格
                        and c.total_invest_budget >= c.cost_price * hold_number
                        
                        union all
                        
                        -- 个股卖出消息
                        select a.id as trading_details_id
                              ,0 as strategy_type
                              ,a.`code`  -- 编码
                              ,a.`name`  -- 名称
                              ,a.zxj  -- 最新价
                              ,null next_price_buy  -- 下一买点
                              ,null as suggest_buy_num -- 建议购买数量
                              ,null as suggest_buy_amt -- 建议购买金额
                              ,a.strategy_id
                              ,d.name as strategy_name  -- 策略名
                              ,c.cost_price -- 当前持仓价格
                              ,round(hold_number,0) as hold_number -- 当前持仓数量
                              ,concat(round(((a.zxj-c.cost_price)/c.cost_price)*100,2),'%') as income_rate -- 当前收益率
                              ,0 as hold_amt_after -- 卖出后持仓金额
                              ,0 as hold_num_after -- 卖出后持仓数量
                              ,0 as price_after -- 卖出后持仓价格
                              ,concat(round(((a.zxj-c.cost_price)/c.cost_price)*100,2),'%') as income_rate_after-- 卖出后收益率
                              ,round(hold_number,0) as suggest_sale_num -- 建议卖出数量
                              ,round(hold_number*a.zxj,0) as suggest_sale_amt -- 建议卖出金额
                              ,round((a.zxj-c.cost_price)*hold_number,2) as income_amt -- 收入金额
                              ,a.user_id 
                              ,0 as is_send
                              ,1 as msg_type
                              ,NOW() as create_time
                              ,NOW() as update_time
                        from stocks_strategy_details a 
                        inner join stocks_selected c on a.selected_id = c.id
                        inner join stocks_strategy d on a.strategy_id = d.id
                        where is_monitor = 1 
                        -- and zxj >= next_price_sell -- 当前价格高于下次卖出价格
                        and ((a.zxj-c.cost_price) * hold_number) >= (c.total_invest_budget * c.income_rate_target)  -- 达到目标收益
                        
                        union all 
                        
                        -- 单笔交易卖出
                        select a.id as trading_details_id
                              ,1 as strategy_type
                              ,a.`code`  -- 编码
                              ,a.`name`  -- 名称
                              ,a.zxj  -- 最新价
                              ,null next_price_buy  -- 下一买点
                              ,null as suggest_buy_num -- 建议购买数量
                              ,null as suggest_buy_amt -- 建议购买金额
                              ,a.strategy_id
                              ,d.name as strategy_name  -- 策略名
                              ,cjjg -- 当前持仓价格
                              ,round(cjsl,0) as hold_number -- 当前持仓数量
                              ,concat(round(((a.zxj-cjjg)/cjjg)*100,2),'%') as income_rate -- 当前收益率
                              ,0 as hold_amt_after -- 卖出后持仓金额
                              ,0 as hold_num_after -- 卖出后持仓数量
                              ,0 as price_after -- 卖出后持仓价格
                              ,concat(round(((a.zxj-cjjg)/cjjg)*100,2),'%') as income_rate_after-- 卖出后收益率
                              ,round(cjsl,0) as suggest_sale_num -- 建议卖出数量
                              ,round(cjsl*a.zxj,0) as suggest_sale_amt -- 建议卖出金额
                              ,round((a.zxj-cjjg)*cjsl,2) as income_amt -- 收入金额
                              ,a.user_id 
                              ,0 as is_send
                              ,1 as msg_type
                              ,NOW() as create_time
                              ,NOW() as update_time
                        from stocks_trading_details a 
                        inner join stocks_selected c on a.selected_id = c.id
                        inner join stocks_strategy d on a.strategy_id = d.id
                        where is_monitor = 1 
                        and zxj >= next_price_sell -- 当前价格高于下次卖出价格
            """
            cursor.execute(update_data)
            data = cursor.fetchall()

            # 插入数据
            insert_data = """
            insert into stock_msg_queue (strategy_details_id, strategy_type, code, name, zxj, next_price_buy, suggest_buy_num, suggest_buy_amt, strategy_id, strategy_name, cost_price, hold_number, income_rate, hold_amt_after, hold_num_after, price_after, income_rate_after, suggest_sale_num, suggest_sale_amt, income_amt, user_id, is_send, msg_type, create_time, update_time)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 插入逻辑
            if data:
                for item in data:
                    # 检查当天是否已存在记录
                    check_sql = """
                                SELECT id 
                                FROM stock_msg_queue 
                                WHERE strategy_details_id = %s 
                                  AND strategy_type = %s 
                                  AND code = %s 
                                  AND msg_type = %s 
                                  AND user_id = %s 
                                  AND DATE(create_time) = CURDATE()
                                """
                    cursor.execute(check_sql, (
                        item['strategy_details_id'],
                        item['strategy_type'],
                        item['code'],
                        item['msg_type'],
                        item['user_id']
                    ))
                    existing = cursor.fetchone()

                    if existing:
                        # 存在则更新
                        update_sql = """
                                    UPDATE stock_msg_queue SET
                                        zxj = %s,
                                        next_price_buy = %s,
                                        suggest_buy_num = %s,
                                        suggest_buy_amt = %s,
                                        strategy_id = %s,
                                        strategy_name = %s,
                                        cost_price = %s,
                                        hold_number = %s,
                                        income_rate = %s,
                                        hold_amt_after = %s,
                                        hold_num_after = %s,
                                        price_after = %s,
                                        income_rate_after = %s,
                                        suggest_sale_num = %s,
                                        suggest_sale_amt = %s,
                                        income_amt = %s,
                                        update_time = NOW()
                                    WHERE id = %s
                                    """
                        cursor.execute(update_sql, (
                            item['zxj'], item['next_price_buy'],
                            item['suggest_buy_num'], item['suggest_buy_amt'],
                            item['strategy_id'], item['strategy_name'],
                            item['cost_price'], item['hold_number'],
                            item['income_rate'], item['hold_amt_after'],
                            item['hold_num_after'], item['price_after'],
                            item['income_rate_after'], item['suggest_sale_num'],
                            item['suggest_sale_amt'], item['income_amt'],
                            existing['id']
                        ))
                    else:
                        # 不存在则插入
                        cursor.execute(insert_data, tuple(item.values()))

            connection.commit()

    except pymysql.MySQLError as e:
        print(f"Error updating A database: {e}")
        connection.rollback()

    finally:
        # 关闭数据库连接
        connection.close()


if __name__ == "__main__":
    msg_queue()
