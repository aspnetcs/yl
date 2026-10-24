# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/4 16:29

@mark    :
"""
import datetime
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from applications.strategy import update_strategy
from applications.scheduler.UpdateStocks import update_stocks, update_stocks_HK
from applications.scheduler.MonitorJob import monitor_msg_data
from applications.scheduler.StockNews import update_stocks_news
from applications.common.libs.monitor.MonitorServer import email_buy, email_sale
from applications.common.libs.tool import is_within_work_hours, c_print
from applications.common.libs.monitor.DingDingServer import ding_buy, ding_sale
from applications.scheduler.UpdateStocks import update_industry_fund_flow
from applications.scheduler.UpdateStocks import update_stocks_analyse
from applications.scheduler.UpdateStocks import update_stocks_kline
from applications.strategy.MsgQueue import msg_queue


def monitor_msg_send():
    """
    股票买卖预警通知
    :return:
    """
    # 获取当前时间
    now = datetime.datetime.now()

    # 检查是否在周一至周五的9:30到15:30之间
    if is_within_work_hours(now):
        data = monitor_msg_data()
        if data:
            # 过滤出需要邮件通知的数据
            filtered_buy_data_mail = [item for item in data if item.get('msg_type') == 0
                                 and item.get('monitor_type') == 0
                                 and item.get('email') is not None
                                 and item.get('email_passwd') is not None]
            filtered_sale_data_mail = [item for item in data if item.get('msg_type') == 1
                                  and item.get('monitor_type') == 0
                                  and item.get('email') is not None
                                  and item.get('email_passwd') is not None]

            if filtered_buy_data_mail:
                try:
                    # 触发买入信息
                    email_buy(filtered_buy_data_mail)
                except Exception as e:
                    print(e)

            if filtered_sale_data_mail:
                try:
                    # 触发卖出信息
                    email_sale(filtered_sale_data_mail)
                except Exception as e:
                    print(e)


            # 过滤需要钉钉通知的数据
            filtered_buy_data_ding = [item for item in data if item.get('msg_type') == 0
                                 and item.get('monitor_type') == 1
                                 and item.get('ding_access_token') is not None
                                 and item.get('ding_secret') is not None]
            filtered_sale_data_ding = [item for item in data if item.get('msg_type') == 1
                                  and item.get('monitor_type') == 1
                                  and item.get('ding_access_token') is not None
                                  and item.get('ding_secret') is not None]

            if filtered_buy_data_ding:
                for i in filtered_buy_data_ding:
                    ding_buy(i)

            if filtered_sale_data_ding:
                for i in filtered_sale_data_ding:
                    ding_sale(i)


def start_scheduler():
    """
    # 配置 定时任务
    :return:
    """
    scheduler = BackgroundScheduler()

    # 更新所有股票列表(A股)
    scheduler.add_job(update_stocks,
                      'cron',
                      hour='9,10,11,13,14,15',  # 覆盖 9:30-11:30 和 13:00-15:30
                      minute='3,8,13,18,23,28,33,38,43,48,53,58',  # 每5分钟执行
                      day_of_week='mon-fri',  # 仅限交易日
                      max_instances=3
                      )

    scheduler.add_job(update_stocks_HK,
                      'cron',
                      hour='9,10,11,13,14,15',  # 覆盖 9:30-11:30 和 13:00-15:30
                      minute='3,8,13,18,23,28,33,38,43,48,53,58',  # 每5分钟执行
                      day_of_week='mon-fri',  # 仅限交易日
                      max_instances=3
                      )

    # 更新所有股票k线数据
    scheduler.add_job(update_stocks_kline,
                      'cron',
                      hour='9,10,11,13,14,15,16',  # 覆盖 9:30-11:30 和 13:00-15:30
                      minute='3',  # 每5分钟执行
                      day_of_week='mon-fri',  # 仅限交易日
                      max_instances=3
                      )

    # 更新板块资金流向
    scheduler.add_job(update_industry_fund_flow,
                      'cron',
                      hour='9,10,11,13,14,15,16',  # 覆盖 9:30-11:30 和 13:00-15:30
                      minute='10',
                      day_of_week='mon-fri',  # 仅限交易日
                      max_instances=3
                      )


    # 每30s策略更新
    scheduler.add_job(update_strategy, IntervalTrigger(seconds=60), max_instances=1)

    # 消息队列
    scheduler.add_job(
        msg_queue,
        'cron',
        hour='9,10,11,13,14,15',  # 覆盖 9:30-11:30 和 13:00-15:30
        minute='1,11,21,31,41,51',  # 每小时的第1和31分钟执行
        day_of_week='mon-fri',  # 仅限工作日
        max_instances=3
    )

    # 通知
    scheduler.add_job(
        monitor_msg_send,
        'cron',
        hour='9,10,11,13,14,15',  # 覆盖 9:30-11:30 和 13:00-15:30
        minute='2,12,22,32,42,52',  # 每小时的第2和32分钟执行
        day_of_week='mon-fri',  # 仅限工作日
        max_instances=3
    )

    # 每天6:30更新个股新闻
    scheduler.add_job(update_stocks_news, 'cron', hour=6, minute=30)

    # 每天10:30更新股票分析宽表
    scheduler.add_job(update_stocks_analyse, 'cron', hour=22, minute=30)


    scheduler.start()

    return scheduler


if __name__ == '__main__':
    monitor_msg_send()
