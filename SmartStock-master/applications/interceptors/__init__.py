# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/11/13 14:19 

@mark    : API拦截器，wx.request发送cookie到hearder，拦截器获取token
'''
from applications.interceptors.ApiAuthInterceptor import before_request as mb_before_request
from applications.interceptors.ApiAuthInterceptor import check_member_login
# from applications.interceptors.AuthInterceptor import before_request
# from applications.interceptors.AuthInterceptor import check_login
# from applications.interceptors.ErrorInterceptor import error_404


def init_itc(app):
    @app.before_request
    def mb_before_request1():
        mb_before_request()

    @app.before_request
    def check_member_login1():
        check_member_login()
