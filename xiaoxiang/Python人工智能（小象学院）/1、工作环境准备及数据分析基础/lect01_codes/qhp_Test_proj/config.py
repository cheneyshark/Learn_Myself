#coding:utf-8

"""
    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    config.py
    功能：     配置文件
"""


import os


# 指定数据集路径
dataset_path = '../lect01_proj/data'
# print(os.path.exists(dataset_path))


# 结果保存路径
output_path = './result'
if not os.path.exists(output_path):
    os.mkdir(output_path)


# 公共列
common_cols = ['year', 'month']


# config.data_config_dict 为提前构造的字典数据
data_config_dict = {'beijing': ('BeijingPM20100101_20151231.csv',
                                ['Dongsi', 'Dongsihuan', 'Nongzhanguan']),
                    'chengdu': ('ChengduPM20100101_20151231.csv',
                                ['Caotangsi', 'Shahepu']),
                    'guangzhou': ('GuangzhouPM20100101_20151231.csv',
                                  ['City Station', '5th Middle School']),
                    'shanghai': ('ShanghaiPM20100101_20151231.csv',
                                 ['Jingan', 'Xuhui']),
                    'shenyang': ('ShenyangPM20100101_20151231.csv',
                                 ['Taiyuanjie', 'Xiaoheyan'])
                    }