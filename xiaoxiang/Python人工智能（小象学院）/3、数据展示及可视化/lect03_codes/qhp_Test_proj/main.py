# coding:utf-8

"""
    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    main.py
    功能：     主程序

    任务：
        - 绘制每个国家指定列的的top10
        - 统计视频发布后上榜的天数
        - 查看views,likes,dislikes,comment_count的关系
"""

import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from pyecharts import Bar, Line, Overlap
import seaborn as sns
import config
import json



def get_chinese_font():
    """
        获取系统中文字体
    """
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')


def combine_video_data():
    """
    将各个国家的数据整合到一起
    :return: --all_video_df--
    """
    video_df_list = []

    for country in config.countries:
        csv_name = country + 'videos.csv'
        csv_path = os.path.join(config.dataset_path, csv_name)
        json_name = country + '_category_id.json'
        json_path = os.path.join(config.dataset_path, json_name)

        # 读取csv数据
        video_df = pd.read_csv(csv_path, index_col='video_id', usecols=config.usecols)

        # 处理csv数据中的时间列
        video_df['trending_date'] = pd.to_datetime(video_df['trending_date'],
                                                   format='%y.%d.%m')
        video_df['publish_time'] = pd.to_datetime(video_df['publish_time'],
                                                  format='%Y-%m-%dT%H:%M:%S.%fZ')
        # 获取发布数据publish_time的日期
        video_df['publish_time'] = pd.to_datetime(video_df['publish_time'].dt.date)

        # 通过json文件获取category_id对应的名称
        category_dict = get_category_from_json(json_path)

        # 将名称添加为对应列
        video_df['category'] = video_df['category_id'].map(category_dict)

        # 添加country列
        video_df['country'] = country

        video_df_list.append(video_df)

    all_video_df = pd.concat(video_df_list)
    all_video_df.to_csv(os.path.join(config.output_path, 'all_videos.csv'))

    return all_video_df


def get_category_from_json(json_path):
    """
    通过json文件获取category_id对应的名称
    :param json_path: json文件的路径
    :return: - category_dict-    category字典
    """
    category_dict = {}

    with open(json_path, 'r') as f:
        data = json.load(f)
        for category in data['items']:
            category_dict[int(category['id'])] = category['snippet']['title']
    return category_dict


def plot_top10_by_country(video_df, col_name, title, save_filename):
    """
        绘制每个国家指定列的的top10
        参数：
            - video_df:         处理后的数据
            - col_name:         列名
            - save_filename:    保存文件名
    """
    fig, axes = plt.subplots(len(config.countries), figsize=(10, 8))
    fig.suptitle(title, fontproperties=get_chinese_font())

    for i, country in enumerate(config.countries):
        country_video_df = video_df[video_df['country'] == country]
        top10_df = country_video_df[col_name].value_counts().sort_values(ascending=False)[:10]

        # 处理x轴的刻度标签
        x_labels = [(label[:7] + '...') if len(label) > 10 else label for label in top10_df.index]

        sns.barplot(x=x_labels, y=top10_df.values, ax=axes[i])
        axes[i].set_xticklabels(x_labels, rotation=45)
        axes[i].set_title(country)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()


def plot_days_to_trend(video_df, save_filename):
    """
    使用pyecharts统计视频发布后上榜的天数
    :param video_df: 处理后的数据
    :param save_filename: 保存文件名
    :return:
    """
    # 新加一行diff作为视频发布后上榜的天数日期
    video_df['diff'] = (video_df['trending_date']-video_df['publish_time']).dt.days
    days_df = video_df['diff'].value_counts()

    # 观察视频发布后两个月的情况
    days_df = days_df[(days_df.index > 0) & (days_df.index <= 60)]
    days_df = days_df.sort_index()
    bar = Bar('视频发布后2个月的情况')
    bar.add('柱状图', days_df.index.tolist(), days_df.values.tolist(),
            is_datazoom_show=True, datazoom_range=[0, 50])

    line = Line()
    line.add('折线图', days_df.index.tolist(), days_df.values.tolist())

    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line)
    overlap.render(os.path.join(config.output_path, save_filename))






def main():
    """
    主程序
    :return:
    """
    # 将各个国家的数据整合到一起
    all_video_df = combine_video_data()

    # 绘制每个国家指定列的的top10
    # plot_top10_by_country(all_video_df, 'category', '各国的类别Top10', 'top10_category.png')

    # 统计视频发布后上榜的天数
    plot_days_to_trend(all_video_df, 'publish_vs_trend.html')


if __name__ == '__main__':
    main()
