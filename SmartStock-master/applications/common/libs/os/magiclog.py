# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/7/17 16:06 

@mark    : 解析EnjoyAPI日志，统计成功和失败记录
'''
import re
from datetime import datetime


# 成功记录
def success_log(log):
    # 初始化正则表达式模式
    pattern_start = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})  INFO \d+ --- \[.+\] (.+?) : 开始执行')
    pattern_datasource = re.compile(r'数据源：(\S+)')
    pattern_sql = re.compile(r'执行SQL：(.*)')
    pattern_end = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})  INFO \d+ --- \[.+\] .+? : 执行结束')

    # 初始化一个列表来存储所有接口的信息
    api_infos = []
    current_api_info = None

    # 遍历日志的每一行
    lines = log.splitlines()
    for line in lines:
        # 查找开始执行的记录
        match_start = pattern_start.search(line)
        if match_start:
            # 如果当前已经有一个接口的信息在处理中，并且找到了新的开始，则先保存当前接口的信息
            if current_api_info:
                api_infos.append(current_api_info)
                # 初始化新的接口信息字典
            current_api_info = {
                'api': match_start.group(2),
                'start_time': match_start.group(1),
                'source': None,
                'execute_sql': None,
                'end_time': None,
                'status': '成功',
                'error_msg': None
            }
            continue

            # 查找数据源记录
        match_datasource = pattern_datasource.search(line)
        if match_datasource and current_api_info:
            current_api_info['source'] = match_datasource.group(1)
            continue

            # 查找执行SQL记录
        match_sql = pattern_sql.search(line)
        if match_sql and current_api_info:
            current_api_info['execute_sql'] = match_sql.group(1)
            continue

            # 查找执行结束记录
        match_end = pattern_end.search(line)
        if match_end and current_api_info:
            current_api_info['end_time'] = match_end.group(1)
            # 将当前接口的信息添加到列表中，并重置current_api_info以便处理下一个接口
            api_infos.append(current_api_info)
            current_api_info = None

        # 如果最后一个接口的执行结束记录之后没有其他接口的记录，则也需要将最后一个接口的信息添加到列表中
    if current_api_info:
        api_infos.append(current_api_info)

    rt = [d for d in api_infos if d.get('end_time') and d['end_time'].strip()]

    return rt


# 失败记录
def error_log(log):
    # 初始化正则表达式模式
    pattern_start = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})  INFO \d+ --- \[.+\] (.+?) : 开始执行')
    pattern_datasource = re.compile(r'数据源：(\S+)')
    pattern_sql = re.compile(r'执行SQL：(.*)')
    pattern_end = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}).*请求出错')
    pattern_error_info = re.compile(r'Caused by: .*?: (.*)')

    # 初始化一个列表来存储所有接口的信息
    api_infos = []
    current_api_info = None

    # 遍历日志的每一行
    lines = log.splitlines()
    for line in lines:
        # 查找开始执行的记录
        match_start = pattern_start.search(line)
        if match_start:
            # 如果当前已经有一个接口的信息在处理中，并且找到了新的开始，则先保存当前接口的信息
            if current_api_info:
                api_infos.append(current_api_info)
                # 初始化新的接口信息字典
            current_api_info = {
                'api': match_start.group(2),
                'start_time': match_start.group(1),
                'source': None,
                'execute_sql': None,
                'end_time': None,
                'status': '失败',
                'error_msg': None
            }
            continue

        # 查找数据源记录
        match_datasource = pattern_datasource.search(line)
        if match_datasource and current_api_info:
            current_api_info['source'] = match_datasource.group(1)
            continue

        # 查找执行SQL记录
        match_sql = pattern_sql.search(line)
        if match_sql and current_api_info:
            current_api_info['execute_sql'] = match_sql.group(1)
            continue

        # 查找执行结束记录
        match_end = pattern_end.search(line)
        if match_end and current_api_info:
            current_api_info['end_time'] = match_end.group(1)
            continue

        # 查找错误信息
        error_info_match = pattern_error_info.search(line)
        if error_info_match and current_api_info:
            current_api_info['error_msg'] = error_info_match.group(1)

            # 将当前接口的信息添加到列表中，并重置current_api_info以便处理下一个接口
            api_infos.append(current_api_info)
            current_api_info = None

        # 如果最后一个接口的执行结束记录之后没有其他接口的记录，则也需要将最后一个接口的信息添加到列表中
    if current_api_info:
        api_infos.append(current_api_info)

    rt = [d for d in api_infos if d.get('end_time') and d['end_time'].strip()]

    return rt


def log_record(log_file):
    # 打开文件
    with open(r'%s' % log_file, 'r') as file:
        file_content = file.read()

    ss = success_log(file_content)
    er = error_log(file_content)

    rt = ss + er

    return rt


# 最近日志
def latest_log(file_list):
    # 初始化最新日期和对应文件名
    latest_date = None

    # 遍历日志文件名称
    for log in file_list:
        # 提取文件名中的日期部分
        date_str = log.split('-')[-1].split('.')[0]  # 假设日期格式是固定的，例如 '20240510'

        # 将字符串日期转换为datetime对象
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            # 如果转换失败（尽管在这个特定例子中不太可能），则跳过当前迭代
            continue

            # 如果当前日期比最新日期更新，则更新最新日期和对应的文件名
        if latest_date is None or date_obj > latest_date:
            latest_date = date_obj
            latest_log_file = log

    return latest_log_file


def insert_overwrite(data, file_name):
    try:
        import pymysql as pymysql
        import traceback
        conn = pymysql.connect(host='10.10.28.30', port=3306, user='root', passwd='root', db='enjoydt')
        cur = conn.cursor()

        # 先删除
        cur.execute("delete from enjoydt.magic_api_log where file_name = '%s'" % file_name)
        conn.commit()

        # 使用预处理语句创建表
        l_data = list(data)  # 获取数据框字段数

        # 插入数据
        sql_a = l_data[0]
        sql_b = '%s'  # str(0 + 1)
        for j in range(1, len(l_data)):
            sql_a += ',' + l_data[j]
            sql_b += ',' + '%s'  # str(j + 1)

        insert_sql = "INSERT INTO enjoydt.magic_api_log " + '(' + sql_a + ')' + ' VALUES ' + '(' + sql_b + ') '

        data = data.replace('nan', '', regex=True)  # 将空值替换为0
        data = data.fillna(value='')  # 空值替换
        data = data.astype(str)  # 全部转为str类型
        data_list = list(map(tuple, data.to_numpy()))

        i = 0
        while i <= len(data_list):
            cur.executemany(insert_sql, data_list[i:i + 999])  # 定量插入，全量会报元组太长的错
            conn.commit()  # 提交数据,否则只存放在缓存，未将值放到数据库

            # print('成功插入%s行，剩余%s行' % (i, len(data_list) - i))

            i = i + 999

        print('完成！成功插入%s表，共%s行' % ("enjoydt.magic_api_log", len(data_list)))

    except:
        traceback.print_exc()


class out_log(object):
    import sys
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    # write()函数这样写，每调用一次就写到记录文件中，不需要等待程序运行结束。
    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass
