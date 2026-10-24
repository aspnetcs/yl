# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/6/24 10:50 

@mark    :
'''
import datetime


# 使用列表推导式和字符串格式化来添加前导零(xxl-job只支持前导零表达式)
def cron_convert(cron_expr):
    parts = cron_expr.split()
    for i in range(len(parts)):
        if i < 4 and all(char.isdigit() for char in parts[i].split(',')):  # 只处理秒、分钟、小时、日字段
            new_part = ','.join(f'{int(num):02d}' for num in parts[i].split(','))
            parts[i] = new_part

    # 重新组合Cron表达式
    cron_expr_with_leading_zeros = ' '.join(parts)

    return cron_expr_with_leading_zeros


# 时间转换成毫秒级Unix时间戳
def to_timestamp(date_time_str):
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    timestamp = int(date_time_obj.timestamp()) * 1000

    return timestamp


def replace_variable(q, replacements):
    import re

    # 使用正则表达式查找所有${xxxxx}变量
    pattern = re.compile(r'\$\{([^}]+)\}')

    # 替换SQL字符串中的变量
    def replace_variables(match):
        var_name = match.group(1)
        return str(replacements.get(var_name, f'${{{var_name}}}'))  # 如果变量名不存在于字典中，则保持原样

    # 应用替换函数
    q_filled = pattern.sub(replace_variables, q)

    # print(q_filled)

    return q_filled


def convert_variable_date(date_param, date_add):
    if date_param == '当前${yyyy-MM-dd HH:mm:ss}':
        result = (datetime.datetime.now() + datetime.timedelta(seconds=date_add * 3600)).strftime('%Y-%m-%d %H:%M:%S')
    elif date_param == '今天${yyyy-MM-dd}':
        result = (datetime.datetime.today() + datetime.timedelta(seconds=date_add * 3600)).strftime('%Y-%m-%d')
    elif date_param == '今天${yyyyMMdd}':
        result = (datetime.datetime.today() + datetime.timedelta(seconds=date_add * 3600)).strftime('%Y%m%d')
    elif date_param == '昨天${yyyy-MM-dd-1}':
        result = (datetime.datetime.today() - datetime.timedelta(days=1) + datetime.timedelta(
            seconds=date_add * 3600)).strftime('%Y-%m-%d')
    elif date_param == '昨天${yyyyMMdd-1}':
        result = (datetime.datetime.today() - datetime.timedelta(days=1) + datetime.timedelta(
            seconds=date_add * 3600)).strftime('%Y%m%d')

    return result


def is_within_work_hours(now=None):
    """
    检查当前时间是否在周一至周五的9:30到12:02 和 13:00到16:02之间
    :param now:
    :return:
    """
    if now is None:
        now = datetime.now()

    # 获取当前是星期几（0=星期一, 6=星期日）
    weekday = now.weekday()

    # 检查是否是周一至周五
    if weekday >= 5:  # 如果weekday是5（星期六）或6（星期日），则不在工作日内
        return False

    # 获取当前的小时和分钟
    current_hour = now.hour
    current_minute = now.minute

    # 检查时间是否在9:30到15:30之间
    if current_hour == 9:
        if current_minute >= 30:
            return True

    elif 10 <= current_hour <= 11:
        return True

    elif current_hour == 12:
        if current_minute <= 2:
            return True

    elif 13 <= current_hour <= 15:
        return True

    elif current_hour == 16:
        if current_minute <= 2:
            return True

    # else:
    #     return True

    return False


def filter_by_json(data, code_to_find):
    """
    从列表中筛选具有特定 code 的字典。

    :param data: 包含多个字典的列表，每个字典有 'code' 键。
    :param code_to_find: 要查找的 code 值。
    :return: 匹配指定 code 的字典列表（在这个例子中只会返回一个或空列表）。
    """
    return [item for item in data if item['code'] == code_to_find]


def c_print(*args, **kwargs):
    """
    自定义的 print 函数，能同时输出时间和信息。

    :param args: 要打印的位置参数
    :param kwargs: 要打印的关键字参数
    """
    # 获取当前时间，并将其格式化为字符串
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 将时间和传入的信息组合成一个字符串
    message = f"[{current_time}] {' '.join(map(str, args))}"
    # 调用内置的 print 函数输出组合后的信息
    print(message, **kwargs, flush=True)


def coalesce(*args):
    """
    从多个参数中返回第一个非空值。
    :param args: 要检查的参数列表
    :return: 第一个非空值，如果所有参数都是空值，则返回 None
    """
    for arg in args:
        if arg is not None:
            return arg
        if arg == '':
            return None
    return None
