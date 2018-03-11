# coding: utf-8

"""
    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    config.py
    功能：     配置文件

"""

import os


# 指定数据集路径
dataset_path = '../lect04_proj/data'


# 使用的特征列
feat_cols = ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep',
             'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time',
             'three_g', 'touch_screen', 'wifi']
# 标签列
label_col = 'price_range'

