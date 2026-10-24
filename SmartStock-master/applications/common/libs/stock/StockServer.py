# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/1/21 17:06

@mark    :
"""
import json
import requests
from applications.config import BaseConfig


def get_stock_list():
    """
    获取所有股票列表(沪深A)
    :return:
    """
    url = f"{BaseConfig.API_BASE_URL}/api/stock/stockList?pageNo=1&pageSize=100"
    headers = {
        "accept": "application/json",
        "apiKey": BaseConfig.API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON数据

        if data["code"] != 200:
            print(f"获取股票列表失败: {data['message']}")
            return None
        else:
            count = data["data"]["count"][0]["count"]
            # print(f"总股票数量: {count}")

            # 分页获取所有股票列表
            total_pages = (count + 49) // 50  # 计算总页数
            all_stock_data = []

            for page in range(1, total_pages + 1):
                url = f"{BaseConfig.API_BASE_URL}/api/stock/stockList?pageNo={page}&pageSize=50"
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                data = response.json()  # 解析JSON数据
                all_stock_data.extend(data["data"]["detail"])
            # print(f"成功获取 {len(all_stock_data)} 条股票数据")
            return all_stock_data

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def get_stock_list_HK():
    """
    获取所有股票列表(港股)
    :return:
    """
    url = f"{BaseConfig.API_BASE_URL}/api/stock/stockList_HK?pageNo=1&pageSize=100"
    headers = {
        "accept": "application/json",
        "apiKey": BaseConfig.API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON数据
        if data["code"] != 200:
            print(f"获取股票列表失败: {data['message']}")
            return None
        else:
            count = data["data"]["count"][0]["count"]
            # print(f"总股票数量: {count}")

            # 分页获取所有股票列表
            total_pages = (count + 49) // 50  # 计算总页数
            all_stock_data = []

            for page in range(1, total_pages + 1):
                url = f"{BaseConfig.API_BASE_URL}/api/stock/stockList_HK?pageNo={page}&pageSize=50"
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                data = response.json()  # 解析JSON数据
                all_stock_data.extend(data["data"]["detail"])
            # print(f"成功获取 {len(all_stock_data)} 条股票数据")
            return all_stock_data

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def get_kline_detail(region, code):
    """
    获取股票k线详情
    :param region:
    :param code:
    :return:
    """
    url = f"{BaseConfig.API_BASE_URL}/api/stock/klineDetail?region={region}&code={code}&pageNo=1&pageSize=50"
    headers = {
        "accept": "application/json",
        "apiKey": BaseConfig.API_KEY
    }
    # print(url)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON数据
        if data["code"] != 200:
            print(f"获取股票k线详情失败: {data['message']}")
            return None
            # print(data)
            count = data["data"]["count"][0]["count"]
            # print(f"总股票数量: {count}")

            # 分页获取所有股票列表
            total_pages = (count + 49) // 50  # 计算总页数
            all_stock_data = []

            for page in range(1, total_pages + 1):
                url = f"{BaseConfig.API_BASE_URL}/api/stock/klineDetail?region={region}&code={code}&pageNo={page}&pageSize=50"
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                data = response.json()  # 解析JSON数据
                all_stock_data.extend(data["data"]["detail"])
            # print(f"成功获取 {len(all_stock_data)} 条股票数据")
            return all_stock_data

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def get_stocks_analyse():
    """
    获取股票分析详情
    :param region:
    :param code:
    :return:
    """
    url = f"{BaseConfig.API_BASE_URL}/api/stock/stocksAnalyse?pageNo=1&pageSize=100"
    headers = {
        "accept": "application/json",
        "apiKey": BaseConfig.API_KEY
    }
    # print(url)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON数据
        if data["code"] != 200:
            print(f"获取股票分析详情失败: {data['message']}")
            return None
        else:
            count = data["data"]["count"][0]["count"]
            # print(f"总股票数量: {count}")

            # 分页获取所有股票列表
            total_pages = (count + 49) // 50  # 计算总页数
            all_stock_data = []

            for page in range(1, total_pages + 1):
                url = f"{BaseConfig.API_BASE_URL}/api/stock/stocksAnalyse?pageNo={page}&pageSize=50"
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                data = response.json()  # 解析JSON数据
                all_stock_data.extend(data["data"]["detail"])
            # print(f"成功获取 {len(all_stock_data)} 条股票数据")
            return all_stock_data

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def get_stocks_industry_fund_flow(date):
    """
    获取股票行业资金流详情
    :return:
    """
    url = f"{BaseConfig.API_BASE_URL}/api/stock/industryFundFlow?reportDate={date}&pageNo=1&pageSize=20"
    headers = {
        "accept": "application/json",
        "apiKey": BaseConfig.API_KEY
    }
    # print(url)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON数据
        if data["code"] != 200:
            print(f"获取股票行业资金流详情失败: {data['message']}")
            return None
        else:
            count = data["data"]["count"][0]["count"]
            # print(f"总股票数量: {count}")
            total_pages = (count + 49) // 50
            all_stock_data = []
            for page in range(1, total_pages + 1):
                url = f"{BaseConfig.API_BASE_URL}/api/stock/industryFundFlow?reportDate={date}&pageNo={page}&pageSize=50"
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                data = response.json()  # 解析JSON数据
                all_stock_data.extend(data["data"]["detail"])

            return all_stock_data

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def get_stock_news():
    """
    获取股票新闻详情
    :return:
    """
    url = f"{BaseConfig.API_BASE_URL}/api/stock/stocksNews?pageNo=1&pageSize=100"
    headers = {
        "accept": "application/json",
        "apiKey": BaseConfig.API_KEY
    }
    # print(url)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON数据
        if data["code"] != 200:
            print(f"获取股票新闻详情失败: {data['message']}")
            return None
        else:
            count = data["data"]["count"][0]["count"]
            # print(f"总股票数量: {count}")
            total_pages = (count + 19) // 20
            all_stock_data = []
            for page in range(1, total_pages + 1):
                url = f"{BaseConfig.API_BASE_URL}/api/stock/stocksNews?pageNo={page}&pageSize=20"
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                data = response.json()  # 解析JSON数据
                all_stock_data.extend(data["data"]["detail"])

            return all_stock_data

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None



if __name__ == "__main__":
    rt = get_stock_list()
    # print(rt)
    # rt = get_kline_detail("GB", "000001,399001,399006,000300,HSI,HSCEI")
    # rt = get_stocks_analyse()
    # rt = get_stocks_industry_fund_flow("2024-12-06")
    # rt = get_stock_news()
    print(rt)

