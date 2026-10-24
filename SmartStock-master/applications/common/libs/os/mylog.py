# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/4/8 9:13 

@mark    :
'''
import logging

class MyLogger:
    """
    自定义日志打印类，将日志保存到`../logs/`目录
    """

    def __init__(self):
        # 创建Logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # 终端Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 文件Handler
        file_handler = logging.FileHandler(
            filename='applications/logs/execute.log',
            mode='a+',
            encoding='UTF-8'
        )
        file_handler.setLevel(logging.NOTSET)

        # Formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s --- %(levelname)s - %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # 添加到Logger中
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


# 生成日志打印实例
LOGGER = MyLogger()

LOGGER.logger.info('...')