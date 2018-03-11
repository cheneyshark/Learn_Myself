# coding:utf-8

"""
    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    config.py
    功能：     配置文件

"""

import os

# 指定数据集路径
dataset_path = '../lect02_proj/data'
# print(os.path.exists(dataset_path))

# 指定输出路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)

# 公共列
common_cols = ['year', 'month', 'day', 'PM_US Post']

# 每个城市对应的文件名及所需分析的列名
# 以字典形式保存，如：{城市：(文件名, 列名)}
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
