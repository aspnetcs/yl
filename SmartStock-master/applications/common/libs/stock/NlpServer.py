# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/10 17:35

@mark    : 大模型
"""

import akshare as ak


def nlp_answer_zs(question):
    """
    目标地址: https://ownthink.com/robot.html

    描述: 思知-对话机器人的接口, 以此来进行智能问答
    :param question:
    :return:
    """
    nlp_answer_df = ak.nlp_answer(question=question)

    return nlp_answer_df

