# import logging
import datetime
from urllib.parse import quote_plus as urlquote


class BaseConfig:
    SUPERADMIN = 'admin'

    SYSTEM_NAME = 'AI量化助理'

    # 上传文件配置
    UPLOADED_PHOTOS_DEST = 'static/upload'
    UPLOADED_FILES_ALLOW = ['gif', 'jpg']
    UPLOADS_AUTOSERVE = True

    # JSON配置
    JSON_AS_ASCII = False

    SECRET_KEY = "sfwfsfdw2443gsdfgsgsfgsdfg343tsvsdff2243fadf"

    # mysql 配置
    MYSQL_USERNAME = "smartstock"
    MYSQL_PASSWORD = "xxxxxx"
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_DATABASE = "smartstock"

    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)  # 会话生命周期
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,  # 连接池大小
        'max_overflow': 5,  # 超出pool_size外最多创建的连接数
        'pool_timeout': 90,  # 连接超时时间（秒）
        'pool_recycle': 360,  # 定期对数据库连接进行回收（秒）
        'pool_pre_ping': True  # 从连接池中取出连接时，检查连接是否可用
    }  # 数据库连接池

    # 默认日志等级
    # LOG_LEVEL = logging.DEBUG

    # flask-mail配置
    MAIL_SERVER = 'smtp.qq.com'
    # MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = 'xxxxx@qq.com'
    MAIL_PASSWORD = 'xxxxx'  # 生成的授权码
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # 插件配置，填写插件的文件名名称，默认不启用插件。
    # PLUGIN_ENABLE_FOLDERS = ["helloworld"]
    PLUGIN_ENABLE_FOLDERS = []

    ######################## 小程序接口配置 ###########################
    MIN_APP = {
        'appid': 'xxxx',
        'appkey': 'xxxx',
        # 商户的key
        'paykey': '',
        # 商户的id号
        'mch_id': '',
        'callback_url': '/api/order/callback'
    }

    # 设置js
    RELEASE_VERSION = {20241206}

    API = {
        'domain': 'http://127.0.0.1:9092'
    }

    UPLOAD = {
        'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
        'prefix_path': '/',
        'prefix_url': '/'
    }

    # 过滤url
    IGNORE_URLS = [
        "^/user/login",
    ]
    API_IGNORE_URLS = [
        "^/api"
    ]

    IGNORE_CHECK_LOGIN_URLS = [
        "^/static",
        "^/favicon.ico"
    ]

    # API 密钥(从https://www.enjoydt.com/获取)
    API_BASE_URL = "https://api.enjoydt.com/"
    API_KEY = "xxxxxxxx"
