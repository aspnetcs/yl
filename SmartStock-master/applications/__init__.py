import os
from flask import Flask
from applications.common.script import init_script
from applications.config import BaseConfig
# from applications.common.logger import register_logger
from applications.extensions import init_plugs
from applications.view import init_bps
from flask_cors import *
from applications.interceptors import init_itc
from applications.scheduler import start_scheduler


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    CORS(app, supports_credentials=True)  # 浏览器允许跨域

    # 引入配置
    app.config.from_object(BaseConfig)

    # 注册flask组件
    init_plugs(app)

    # 注册蓝图
    init_bps(app)

    # 注册命令
    init_script(app)

    # 注册小程序会员登录拦截器
    init_itc(app)

    # 定时调度
    start_scheduler()

    # # 日志
    # register_logger(app)

    return app
