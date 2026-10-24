# -*- coding: utf-8 -*-
import time
from applications.config import BaseConfig


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    # 设置js时时更新
    @staticmethod
    def buildStaticUrl(path):
        release_version = BaseConfig.RELEASE_VERSION
        ver = "%s" % (int(time.time())) if not release_version else release_version
        path = "/static" + str(path) + "?ver=" + str(ver)
        return UrlManager.buildUrl(path)

    # 相片的url设置
    @staticmethod
    def buildImageUrl(path):
        app_config = BaseConfig.API['domain']
        url = app_config + BaseConfig.UPLOAD['prefix_url'] + path
        return url
