# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/1/10 13:43 

@mark    :日期处理函数
'''
import datetime


def is_timestamp(s):
    try:
        datetime.datetime.fromtimestamp(float(s))
        return True
    except ValueError:
        return False

