# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/25 15:28

@mark    : 重新训练情感分析模型
"""
from snownlp import seg
from snownlp import SnowNLP
from snownlp import sentiment
import os
# 获取项目根目录
project_root = os.path.dirname(os.path.abspath('__file__'))
data_folder = os.path.join(project_root, 'applications/nlp/data')
neg_file_path = os.path.join(data_folder, 'neg.txt')
pos_file_path = os.path.join(data_folder, 'pos.txt')

# 训练用户提供的自定义的新的训练分词词典的负面情感数据集和正面情感数据集
sentiment.train(neg_file_path,pos_file_path)
sentiment.save(f'{data_folder}/sentiment2.marshal')  # 保存训练后的模型
print(sentiment.data_path) # 查看or设置snownlp提供的默认情感分析模型的路径


