# -*- coding: utf-8 -*-

"""
    作者:     Robin
    版本:     1.0
    日期:     2018/02
    文件名:    config.py
    功能：     配置文件

    声明：小象学院拥有完全知识产权的权利；只限于善意学习者在本课程使用，
         不得在课程范围外向任何第三方散播。任何其他人或机构不得盗版、复制、仿造其中的创意，
         我们将保留一切通过法律手段追究违反者的权利
"""
import os

# 指定数据集路径
dataset_path = './data'

# 结果保存路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)

countries = ['CA', 'DE', 'GB', 'US']

# 使用的列
usecols = ['video_id', 'trending_date', 'channel_title', 'category_id', 'publish_time', 'views', 'likes',
           'dislikes', 'comment_count', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed']
