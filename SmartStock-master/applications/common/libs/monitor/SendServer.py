# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/7 17:39

@mark    :
"""
from applications.config import BaseConfig


def send_mail(html_msg, to_list, title):
    """
    # 自定义函数
    :param html_msg: html_msg=rendered_content
    :param to_list: to_list=i["email"]
    :param title: title='股票买入通知'
    :return:
    """
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import smtplib

    subject = title
    nickname = "SmartStock"
    sender = BaseConfig.MAIL_USERNAME  # 发送邮件人
    mail_pass = BaseConfig.MAIL_PASSWORD  # 密码

    msg = MIMEMultipart()  # 将不同类型的内容进行分段式存储，
    msg['Subject'] = subject  # 邮件主题
    msg['From'] = f"{nickname} <{sender}>"  # 发件人
    msg['To'] = ",".join([to_list])  # 收件人
    try:
        html = html_msg
        content = MIMEText(html, 'html', 'utf-8')  # 正文内容
        msg.attach(content)  # 将正文内容存储在msg中

        s = smtplib.SMTP_SSL(BaseConfig.MAIL_SERVER, BaseConfig.MAIL_PORT)  # SMTP_SSL发送邮件用的，所发邮件的交付主机邮箱，465接口
        s.login(sender, mail_pass)  # 登录自己本邮箱
        s.send_message(msg)  # 发送附件、正文信息、主题、发件人邮箱，邮件人邮箱等等
        s.close()  # 关闭邮件发送与所发邮件主机接口
        # print('发送成功')

        return True  # 如果没有问题返回True

    except smtplib.SMTPException as e:
        print(e)
        return False  # 否则返回False

