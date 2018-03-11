# coding:utf-8

"""

    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    Test.py
    功能：     按小时统计每个城市的PM2.5指数，并添加相应的污染状态

    依赖：     config.py
"""

import os
import pandas as pd
import numpy as np
import config


def data_nan_drop(city_data, cityname):
    """
    去掉数据中带有nan的数据
    :param city_data: city_data
    :return: droped_data
    """
    data_drop = city_data.dropna()
    # 重置索引
    data_drop = data_drop.reset_index(drop=True)
    # 添加一个列'city' 作为对应的城市名
    data_drop['city'] = cityname

    return data_drop


def get_ch_us_pm(data, areas):
    """
    将中国各个地区的数据做均值并放入一个新列 PM_China 中
    :param data: 去空值后的数据
    :return: data_ch_us   并只保留PM_China 和 PM_US 的PM数据
    """
    areas_ch = ['PM_' + area for area in areas]
    data['PM_China'] = data[areas_ch].mean(axis=1)
    data = data[['year', 'month', 'day', 'hour', 'city', 'PM_China', 'PM_US Post']]

    return data


def date_combine(data):
    """
    将'year', 'month', 'day'合并成字符串列'date'
    :param data: 合并了5个城市后的数据
    :return: dated_data
    """
    dated_data = data.copy()
    dated_data[['year', 'month', 'day', 'hour']] = dated_data[['year', 'month', 'day', 'hour']].astype('str')
    dated_data['date'] = dated_data['year'].str.cat([dated_data['month'], dated_data['day'], dated_data['hour']], sep='-')
    dated_data = dated_data.drop(['year', 'month', 'day', 'hour'], axis=1)

    return dated_data

def main():
    """
    主函数
    :return:
    """
    data = []

    for cityname, [filename, areas] in config.data_config_dict.items():
        city_path = os.path.join(config.dataset_path, filename)
        usecols = config.common_cols + ['hour'] + ['PM_' + area for area in areas]

        # 读取数据
        city_data = pd.read_csv(city_path, usecols=usecols) if \
            os.path.exists(city_path) else print('{}文件位置错误'.format(cityname))

        # 去空值
        city_data = data_nan_drop(city_data, cityname)

        # 处理获取中国与美国统计的PM数据
        city_data_ch_us = get_ch_us_pm(city_data, areas)
        data.append(city_data_ch_us)

    all_data_df = pd.concat(data)

    # 将'year', 'month', 'day'合并成字符串列'date'
    all_data_df = date_combine(all_data_df)
    day_stats = all_data_df.groupby(['city', 'date'])[['PM_China', 'PM_US Post']].mean()
    day_stats.reset_index(inplace=True)
    print(day_stats)



if __name__ == '__main__':
    main()
