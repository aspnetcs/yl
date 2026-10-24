# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/8/1 18:41 

@mark    :
'''
import logging
from logging.handlers import TimedRotatingFileHandler


def register_logger(app):
    # 确保日志目录存在
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 移除所有现有的 StreamHandler
    for handler in list(app.logger.handlers):
        if isinstance(handler, logging.StreamHandler):
            app.logger.removeHandler(handler)

            # 创建一个 FileHandler，每天轮转日志文件，并保留7天的备份
    file_handler = logging.handlers.TimedRotatingFileHandler(
        'logs/enjoydt.log', when='D', interval=1, backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    print('..........................................')
    print(app.logger.handlers)
    print('++++++++++++++++++++++++++++++++++++++++++++')
    # 设置 Flask 应用日志器的级别并添加 FileHandler
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    print('..........................................')
    print(app.logger.handlers)
    print('++++++++++++++++++++++++++++++++++++++++++++')


