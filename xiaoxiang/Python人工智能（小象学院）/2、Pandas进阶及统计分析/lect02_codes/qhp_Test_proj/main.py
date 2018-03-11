# coding:utf-8

"""
    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    main.py
    功能：     主程序

    实战案例1-2：中国五大城市PM2.5数据分析 (2)
    任务：
        - 统计每个城市每天的平均PM2.5的数值
        - 基于天数对比中国环保部和美国驻华大使馆统计的污染状态

"""

import os
import numpy as np
import pandas as pd
import config


def preprocess_data(data_df, city_name):
    """
    :param data_df: 数据集
    :param city_name: 城市名称
    :return: 预处理后的数据集 （去掉包含NaN的行）
    """
    cln_data_df = data_df.dropna()
    # 重置索引  丢弃删掉的索引
    cln_data_df = cln_data_df.reset_index(drop=True)
    # 添加一列作为城市名
    cln_data_df['city'] = city_name
    # print('{}城市预处理数据预览：{}'.format(city_name, cln_data_df.head()))

    return cln_data_df


def get_china_us_pm_df(cln_data_df, suburb_cols):
    """

    :param cln_data_df: 去空后的数据
    :param suburb_cols: 每个城市中国PM数据点名称
    :return: 处理后的中国与美国PM数据
    """
    pm_suburb_cols = ['PM_' + col for col in suburb_cols]

    # 取PM的均值为中国环保部在该城市的测量值
    cln_data_df['PM_China'] = cln_data_df[pm_suburb_cols].mean(axis=1)
    proc_data_df = cln_data_df[['city', 'PM_China'] + config.common_cols]
    # print('{}城市处理后的中美PM数据预览:\n{}'.format(proc_data_df['city'][0], proc_data_df.head()))
    return proc_data_df


def add_date_col_to_df(all_data_df):
    """
    'year', 'month', 'day'合并成字符串列'date'
    :param all_data_df: PM数据
    :return: proc_data_df --合并data后的数据
    """
    data_df = all_data_df.copy()

    # 把年月日转换为字符串
    data_df[['year', 'month', 'day']] = data_df[['year', 'month', 'day']].astype('str')
    # 合并列
    data_df['date'] = data_df['year'].str.cat([data_df['month'], data_df['day']], sep='-')
    # 去除列
    data_df = data_df[['date', 'city', 'PM_China', 'PM_US Post']]

    return data_df


def add_polluted_state_col_to_df(day_stats):
    """
    根据每天的PM值，添加相关的污染状态
    :param day_stats: 按城市，天归类后的数据
    :return: --proc_day_stats--  添加污染状态后的数据
    """
    proc_day_stats = day_stats.copy()
    bins = [-np.inf, 35, 75, 150, np.inf]
    labels = ['good', 'light', 'medium', 'heavy']

    proc_day_stats['Pollution PM_China'] = pd.cut(proc_day_stats['PM_China'], bins=bins, labels=labels)
    proc_day_stats['Pollution PM_US'] = pd.cut(proc_day_stats['PM_US Post'], bins=bins, labels=labels)
    return proc_day_stats


def compare_state_by_day(day_stats):
    """
    基于天数对比中国环保部和美国驻华大使馆统计的污染状态
    :param day_stats: 包含每天污染状态的数据
    :return: comparison_result
    """
    city_names = config.data_config_dict.keys()
    city_comparison_list = []
    for city in city_names:
        city_df = day_stats[day_stats['city'] == city]
        # 统计类别个数
        city_polluted_days_count_ch = pd.value_counts(city_df['Pollution PM_China']).to_frame(name=city + '_CH')
        city_polluted_days_count_us = pd.value_counts(city_df['Pollution PM_US']).to_frame(name=city + '_US')
        city_comparison_list.append(city_polluted_days_count_ch)
        city_comparison_list.append(city_polluted_days_count_us)

    comparison_result = pd.concat(city_comparison_list, axis=1)
    return city_comparison_list





def main():
    """
        主函数
    :return:null
    """
    city_data_list = []

    # 提取出配置文件中的城市文件名、所需列表
    for city_name, (filename, suburb_cols) in config.data_config_dict.items():
        data_file = os.path.join(config.dataset_path, filename)
        usecols = config.common_cols + ['PM_' + col for col in suburb_cols]
        # 读取数据
        data_df = pd.read_csv(data_file, usecols=usecols)

        # 数据预处理
        cln_data_df = preprocess_data(data_df, city_name)

        # 处理获取中国与美国统计的PM数据
        proc_data_df = get_china_us_pm_df(cln_data_df, suburb_cols)
        city_data_list.append(proc_data_df)

    # 合并5个城市的处理后的数据 （多个pandas append出来的是一个list类型数据，需要通过concat变成一个DataFrame）
    all_data_df = pd.concat(city_data_list)

    # 将'year', 'month', 'day'合并成字符串列'date'
    all_data_df = add_date_col_to_df(all_data_df)

    # === Step 3. 数据分析 ===
    # 通过分组操作获取每个城市每天的PM均值
    # 统计每个城市每天的平均PM2.5的数值
    day_stats = all_data_df.groupby(['city', 'date'])[['PM_China', 'PM_US Post']].mean()

    # 分组操作后day_stats的索引为层级索引['city', 'date']，
    # 为方便后续分析，将层级索引转换为普通列
    day_stats.reset_index(inplace=True)

    # 根据每天的PM值，添加相关的污染状态
    day_stats = add_polluted_state_col_to_df(day_stats)
    # 基于天数对比中国环保部和美国驻华大使馆统计的污染状态
    comparison_result = compare_state_by_day(day_stats)
    print(comparison_result)

if __name__ == '__main__':
    main()
