# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/6 16:23

@mark    :
"""
import time
import random
import datetime
from applications.strategy.Pyramid import pyramid_5
from applications.common.libs.tool import is_within_work_hours, c_print
from applications.strategy.MonitorPrice import monitorPrice
from applications.strategy.GridTrading import positive_t
from applications.strategy.MsgQueue import msg_queue

def update_strategy():
    """
    定期更新策略信息
    :return:
    """

    try:
        # 添加随机延迟，避免多个策略同时启动
        time.sleep(random.uniform(0.1, 0.5))

        # 金字塔5策略
        c_print("开始执行金字塔策略...")
        pyramid_5()
        time.sleep(1)

        # 监控到价
        c_print("开始执行监控到价策略...")
        monitorPrice()
        time.sleep(1)

        # 网格交易(正T)
        c_print("开始执行网格交易策略...")
        positive_t()


        c_print("所有策略更新完成")

    except Exception as e:
        c_print(f"策略更新过程中发生错误: {str(e)}")


if __name__ == "__main__":
    update_strategy()
