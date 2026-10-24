"""
Create Time : 2022/8/10 10:14 

Author : leven

Mark ： 系统操作函数
"""
import datetime
import random
import string


#######################创建目录#############################
def mkdir(path):
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


################################  日志记录  ####################################
import sys


class out_log(object):
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


# sys.stdout = out_log('output.log', sys.stdout)           # 将输出记录到log
# sys.stderr = out_log('output.log_file', sys.stderr)		# 将错误信息记录到log_file


################################  根据当前时间随机生成文件名  ####################################
def random_file_name(file_type):
    # 获取当前时间
    now = datetime.datetime.now()

    # 格式化当前时间，用于作为文件名的一部分
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # 生成一个随机的字符串，用于作为文件名的另一部分
    random_part = ''.join(random.choices(string.ascii_lowercase, k=10))

    # 拼接文件名
    filename = f"{timestamp}_{random_part}.%s" % file_type

    # 打印生成的文件名
    # print(log_filename)

    # 如果需要，你可以在这里打开文件并写入日志
    # with open(log_filename, 'a') as log_file:
    #     log_file.write("Some log message\n")
    return filename
