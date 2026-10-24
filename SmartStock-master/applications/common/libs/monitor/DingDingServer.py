# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/24 13:28

@mark    :
"""
import requests
import json
import base64
import hmac
import hashlib
import time


def ding_sale(data):
    """
    发送钉钉机器人消息:markdown形式
    :param access_token:
    :param text:
    :return:
    """
    try:
        access_token = data["ding_access_token"]
        secret = data["ding_secret"]
        # 当前时间戳
        timestamp = str(round(time.time() * 1000))

        # 拼接字符串
        string_to_sign = '{}\n{}'.format(timestamp, secret)

        # 生成签名
        sign = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(sign).decode('utf-8')

        # 钉钉机器人的Webhook URL
        webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(access_token,
                                                                                                         timestamp,
                                                                                                         sign)
        title = "股票【卖出】通知"
        text = f'''
### 股票【卖出】通知

尊敬的投资者：
根据您的投资策略【{data["strategy_id"]}{data["strategy_name"]}】，提醒您卖出**{data["name"]}**，具体卖出建议如下：

**股票编码：** {data["code"]}

**股票名称：** {data["name"]}

**最新价格：** {data["zxj"]}

**当前持仓量：** {data["hold_number"]}

**当前持仓价：** {data["cost_price"]}

**当前收益率：** {data["income_rate"]}

-----------------------------------------------
**建议卖出股数：** {data["hold_number"]}

**建议卖出总额：** {data["suggest_sale_amt"]}

**卖出后收益：** {data["income_amt"]}

请定期检查您的投资组合，并根据市场情况做出适当调整。如有任何疑问或需要进一步的帮助，请随时联系我们的客服团队。

祝您投资顺利！

*注：本消息为自动发送，请勿回复。*
'''

        # 构建消息内容
        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }

        # 发送POST请求
        response = requests.post(webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})

        # 检查响应状态码
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                print("钉钉消息发送成功")
            else:
                print(f"钉钉消息发送失败，错误码: {result.get('errcode')}，错误信息: {result.get('errmsg')}")
        else:
            print(f"请求失败，状态码: {response.status_code}，响应内容: {response.text}")

        return response.json()

    except Exception as e:
        print(e)


def ding_buy(data):
    """
    发送钉钉机器人消息:markdown形式
    :param access_token:
    :param text:
    :return:
    """
    try:
        access_token = data["ding_access_token"]
        secret = data["ding_secret"]
        # 当前时间戳
        timestamp = str(round(time.time() * 1000))

        # 拼接字符串
        string_to_sign = '{}\n{}'.format(timestamp, secret)

        # 生成签名
        sign = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(sign).decode('utf-8')

        # 钉钉机器人的Webhook URL
        webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(access_token,
                                                                                                         timestamp,
                                                                                                         sign)
        title = "股票【买入】通知"
        text = f'''
### 股票【买入】通知

尊敬的投资者：
根据您的投资策略【{data["strategy_id"]}{data["strategy_name"]}】，提醒您买入**{data["name"]}**，具体买入建议如下：

**股票编码：** {data["code"]}

**股票名称：** {data["name"]}

**最新价格：** {data["zxj"]}

**当前持仓量：** {data["hold_number"]}

**当前持仓价：** {data["cost_price"]}

**当前收益率：** {data["income_rate"]}

-----------------------------------------------
**建议买入股数：** {data["suggest_buy_num"]}

**建议买入总额：** {data["suggest_buy_amt"]}

**买入后持仓股数：** {data["hold_num_after"]}

**买入后持仓金额：** {data["hold_amt_after"]}

**买入后持仓价格：** {data["price_after"]}

**买入后收益率：** {data["income_rate_after"]}

请定期检查您的投资组合，并根据市场情况做出适当调整。如有任何疑问或需要进一步的帮助，请随时联系我们的客服团队。

祝您投资顺利！

*注：本消息为自动发送，请勿回复。*
'''

        # 构建消息内容
        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }

        # 发送POST请求
        response = requests.post(webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})

        # 检查响应状态码
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                print("钉钉消息发送成功")
            else:
                print(f"钉钉消息发送失败，错误码: {result.get('errcode')}，错误信息: {result.get('errmsg')}")
        else:
            print(f"请求失败，状态码: {response.status_code}，响应内容: {response.text}")

        return response.json()

    except Exception as e:
        print(e)


