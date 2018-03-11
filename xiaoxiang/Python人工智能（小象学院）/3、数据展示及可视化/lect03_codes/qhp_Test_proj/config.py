# coding:utf-8

"""
    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    config.py
    功能：     配置文件
"""

import os


# 指定数据集地址
dataset_path = '../lect03_proj/data'

# 指定输出结果地址
output_path = './output'
if not os.path.exists(output_path):
    os.mkdir(output_path)

countries = ['CA', 'DE', 'GB', 'US']

# 使用的列
usecols = ['video_id', 'trending_date', 'channel_title', 'category_id', 'publish_time', 'views', 'likes',
           'dislikes', 'comment_count', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed']