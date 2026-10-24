# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/7 16:40

@mark    :
"""
from jinja2 import Template
from applications.common.libs.monitor.SendServer import send_mail


def email_buy(dataList):

    # 指定HTML文件的路径
    file_path = 'templates/strategy/monitor/emailBuy.html'

    # 读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用Jinja2处理模板
    template = Template(html_content)

    for i in dataList:

        rendered_content = template.render(i)

        try:
            send_mail(rendered_content, i["email"], '股票买入通知')
            print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败：{e}")


def email_sale(dataList):

    # 指定HTML文件的路径
    file_path = 'templates/strategy/monitor/emailSale.html'

    # 读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用Jinja2处理模板
    template = Template(html_content)

    for i in dataList:

        rendered_content = template.render(i)

        try:
            send_mail(rendered_content, i["email"], '股票卖出通知')
            print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败：{e}")


if __name__ == "__main__":
    data = ''
    email_buy(data)
