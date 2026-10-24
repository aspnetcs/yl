from functools import wraps
from flask import abort, request, jsonify, session, current_app, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from applications.common.admin_log import admin_log


def authorize(power: str, log: bool = False):
    """用户权限判断，用于判断目前会话用户是否拥有访问权限

    :param power: 权限标识
    :type power: str
    :param log: 是否记录日志, defaults to False
    :type log: bool, optional
    """

    def decorator(func):
        @login_required
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查权限列表是否存在
            permissions = session.get('permissions')
            if permissions is None:
                # 如果权限信息为None，可能是会话过期或未正确设置权限,重定向到登录页面
                flash("会话信息已过期，请重新登录。", "error")
                logout_user()
                # 从会话中移除权限信息
                if 'permissions' in session:
                    session.pop('permissions')
                return redirect(url_for('system.passport.login'))  # 重定向到登录页面

            # 管理员不做权限判断
            if current_user.username == current_app.config.get("SUPERADMIN"):
                return func(*args, **kwargs)

            # 检查用户是否有指定的权限
            if not power in session.get('permissions'):
                if log:
                    admin_log(request=request, is_access=False)
                if request.method == 'GET':
                    abort(403)
                else:
                    return jsonify(success=False, msg="权限不足!")

            # 写入操作日志
            if log:
                admin_log(request=request, is_access=True)

            return func(*args, **kwargs)

        return wrapper

    return decorator
