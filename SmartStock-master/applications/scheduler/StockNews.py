# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/12 11:18

@mark    : 舆情分析
"""
import pymysql
import json
import datetime
from snownlp import SnowNLP
from applications.config import BaseConfig
from applications.common.libs.tool import c_print
from applications.common.libs.stock.StockServer import get_stock_news


def update_stocks_news():
    """
    每天8:00更新股票新闻列表到数据库表stocks_news
    :return:
    """
    c_print("开始更新股票新闻")

    # 数据库连接配置
    db_config = {
        'host': BaseConfig.MYSQL_HOST,
        'user': BaseConfig.MYSQL_USERNAME,
        'password': BaseConfig.MYSQL_PASSWORD,
        'db': BaseConfig.MYSQL_DATABASE,
        'charset': 'utf8mb4',  # 确保支持Unicode字符
        'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式的游标
    }

    # 连接到数据库
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:

            # 获取股票新闻详情
            news_list = get_stock_news()

            c_print("插入数据库")
            # 删除旧数据
            delete_query = "DELETE FROM stocks_news"
            cursor.execute(delete_query)
            # 提交事务
            connection.commit()

            # 表结构与JSON中的键匹配
            insert_sql = """
            INSERT INTO stocks_news (code, name, title, contents, publish_time, act_source, url, is_hot, update_time, positive_prob, negative_prob, sentiment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # 遍历JSON列表并执行插入操作
            for record in news_list:
                # 提取字段值
                values = (
                    record['code'],
                    record['name'],
                    record['title'],
                    record['contents'],
                    record['publish_time'],
                    record['act_source'],
                    record['url'],
                    record['is_hot'],
                    record['update_time'],
                    record['positive_prob'],
                    record['negative_prob'],
                    record['sentiment']
                )
                # 注意：这里需要确保record中的键与insert_sql中的占位符顺序一致
                # 或者你可以使用命名参数（如果数据库驱动支持）来避免顺序问题
                cursor.execute(insert_sql, values)

            # 提交事务
            connection.commit()

            c_print("成功更新股票新闻stocks_news")

            connection.close()

    except pymysql.MySQLError as e:
        c_print("更新股票新闻stocks_news失败：", str(e))
        return []


if __name__ == '__main__':
    update_stocks_news()
