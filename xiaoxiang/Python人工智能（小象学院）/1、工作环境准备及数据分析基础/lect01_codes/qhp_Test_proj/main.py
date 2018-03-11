# coding:utf-8

"""
    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    main.py
    功能：     主程序

    实战案例1-1：中国五大城市PM2.5数据分析 (1)
    任务：
        - 五城市污染状态
        - 五城市每个区空气质量的月度差异
"""

import config
import csv
import os
import numpy as np
# 控制numpy打印不为科学计数法   ======================
np.set_printoptions(suppress=True)

def load_data(data_file, usecols):
    """
        读取数据文件，加载数据
        参数：
            - data_file:    文件路径
            - usecols:      所使用的列
        返回：
            - data_arr:     数据的多维数组表示
    """
    data = []
    # 读取需要的数据并存入data中
    with open(data_file, 'r') as csvfile:
        data_read = csv.DictReader(csvfile)
        for row in data_read:
            row_data = []
            for col in usecols:
                string_value = row[col]
                row_data.append(float(string_value) if string_value != 'NA' else np.nan)
            if not any(np.isnan(row_data)):
                data.append(row_data)

    # 将data转换为ndarray
    data_arr = np.array(data)
    return data_arr


def get_polluted_perc(data_arr):
    """
        获取污染占比的小时数
        规则：
            重度污染(heavy)     PM2.5 > 150
            重度污染(medium)    75 < PM2.5 <= 150
            轻度污染(light)     35 < PM2.5 <= 75
            优良空气(good)      PM2.5 <= 35
        参数：
            - data_arr: 数据的多维数组表示
        返回：
            - polluted_perc_list: 污染小时数百分比列表
    """
    # 对各个地区的污染取平均数作为城市对应小时的污染程度
    hour_val = np.mean(data_arr[:, 2:], axis=1)
    hours_num = hour_val.shape[0]

    heavy_hours = hour_val[hour_val > 150].shape[0]
    medium_hours = hour_val[(hour_val <= 150) & (hour_val > 75)].shape[0]
    light_hours = hour_val[(hour_val <= 75) & (hour_val > 35)].shape[0]
    good_hours = hour_val[hour_val <= 35].shape[0]

    polluted_perc_list = [heavy_hours/hours_num, medium_hours/hours_num,
                          light_hours/hours_num, good_hours/hours_num]
    # print('polluted_perc_list:', type(polluted_perc_list), polluted_perc_list)
    return polluted_perc_list


def get_avg_pm_per_month(data_arr):
    """
        获取每个区每月的平均PM值
        参数：
            - data_arr: 数据的多维数组表示
        返回：
            - results_arr:  多维数组结果
    """
    results = []
    years = np.unique(data_arr[:,0])
    for year in years:
        year_data_arr = data_arr[data_arr[:, 0] == year]
        months = np.unique(year_data_arr[:,1])

        for month in months:
            month_data_arr = year_data_arr[year_data_arr[:, 1] == month]
            month_vals = np.mean(month_data_arr[:, 2:], axis=0)

            row_data = ['{:.0f}-{:02.0f}'.format(year, month)] + month_vals.tolist()
            results.append(row_data)

    result_array = np.array(results)
    return result_array


def main():
    """
        主函数
    """
    polluted_state_list = []

    for city_name, (filename, cols) in config.data_config_dict.items():
        # print('city_name:', city_name, type(city_name), 'filename:', filename, type(filename), 'cols:', cols, type(cols))

        # === Step 1+2. 数据获取 + 数据处理 ===
        data_file_path = os.path.join(config.dataset_path, filename)
        use_cols = config.common_cols + ['PM_' + col for col in cols]
        data_arr = load_data(data_file_path, use_cols)

        print('{}共有{}行数据'.format(city_name, data_arr.shape[0]))
        # print('{}城市的数据预览为:\n{}'.format(city_name,data_arr[:10]))

        # 计算五城市污染状态
        polluted_perc_list = get_polluted_perc(data_arr)
        polluted_state_list.append([city_name] + polluted_perc_list)
        print('{}污染小时数占比：{}'.format(city_name,polluted_perc_list))

        # 五城市每个区空气质量的月度差异
        results_arr = get_avg_pm_per_month(data_arr)


if __name__ == '__main__':
    main()
