# -*- coding: utf-8 -*-
from applications.common.libs.Helper import ops_render
from applications.common.libs.LogService import LogService


def error_404(e):
    LogService.addErrorlog(str(e))
    return ops_render('error/error.html', {'status': 404, 'msg': '很抱歉！您访问的页面不存在'})
