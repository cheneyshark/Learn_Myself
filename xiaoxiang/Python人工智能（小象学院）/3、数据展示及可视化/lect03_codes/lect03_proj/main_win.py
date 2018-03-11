# -*- coding: utf-8 -*-

"""
    作者:     Robin
    版本:     1.0
    日期:     2018/02
    文件名:    main.py
    功能：     主程序

    实战案例2：YouTube视频趋势分析
    任务：
        - 绘制每个国家指定列的的top10
        - 统计视频发布后上榜的天数
        - 查看views,likes,dislikes,comment_count的关系

    数据集来源：https://www.kaggle.com/datasnaek/youtube-new

    声明：小象学院拥有完全知识产权的权利；只限于善意学习者在本课程使用，
         不得在课程范围外向任何第三方散播。任何其他人或机构不得盗版、复制、仿造其中的创意，
         我们将保留一切通过法律手段追究违反者的权利
"""

import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts import Bar, Line, Overlap


import config


# 解决matplotlib显示中文问题
# 仅适用于Windows
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def get_category_from_json(json_file):
    """
        通过对应的json文件获取 category_id - category_title
        参数:
            - json_file:    json文件路径
        返回:
            - category_dict:    category字典
    """
    category_dict = {}

    with open(json_file, 'r') as f:
        data = json.load(f)
        for category in data['items']:
            category_dict[int(category['id'])] = category['snippet']['title']
    return category_dict


def combine_video_data():
    """
        将各个国家的数据整合到一起
        返回：
            - all_video_df: 所有国家的数据
    """
    video_df_list = []

    for country in config.countries:
        print('数据处理：', country)
        csv_filename = country + 'videos.csv'
        json_filename = country + '_category_id.json'
        video_df = pd.read_csv(os.path.join(config.dataset_path, csv_filename),
                               index_col='video_id', usecols=config.usecols)
        # 处理时间列
        video_df['trending_date'] = pd.to_datetime(video_df['trending_date'], format='%y.%d.%m')
        video_df['publish_time'] = pd.to_datetime(video_df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')

        # 获取发布的日期
        video_df['publish_date'] = video_df['publish_time'].dt.date
        video_df['publish_date'] = pd.to_datetime(video_df['publish_time'])

        # 通过json文件获取category_id对应的名称
        category_dict = get_category_from_json(os.path.join(config.dataset_path, json_filename))

        # 通过map操作添加category名称列
        video_df['category'] = video_df['category_id'].map(category_dict)

        # 添加country列
        video_df['country'] = country

        video_df_list.append(video_df)

        # 预览数据
        print('数据预览：')
        print(video_df.head())

    all_video_df = pd.concat(video_df_list)
    # 保存结果到一个数据集中
    all_video_df.to_csv(os.path.join(config.output_path, 'all_videos.csv'))

    return all_video_df


def plot_top10_by_country(video_df, col_name, title, save_filename):
    """
        绘制每个国家指定列的的top10
        参数：
            - video_df:         处理后的数据
            - col_name:         列名
            - save_filename:    保存文件名
    """
    fig, axes = plt.subplots(len(config.countries), figsize=(10, 8))
    # 为整幅图添加标题
    fig.suptitle(title)

    for i, country in enumerate(config.countries):
        country_video_df = video_df[video_df['country'] == country]
        # 获取指定列的top10
        top10_df = country_video_df[col_name].value_counts().sort_values(ascending=False)[:10]

        # 处理x轴的刻度标签
        x_labels = [label[:7] + '...' if len(label) > 10 else label for label in top10_df.index]

        # 制图
        sns.barplot(x=x_labels, y=top10_df.values, ax=axes[i])
        axes[i].set_xticklabels(x_labels, rotation=45)
        axes[i].set_title(country)
    plt.tight_layout()

    # 为子图顶部增加间隔，防止子图的标题和整幅图的标题重叠
    plt.subplots_adjust(top=0.9)
    plt.savefig(os.path.join(config.output_path, save_filename))
    plt.show()


def plot_days_to_trend(video_df, save_filename):
    """
        使用pyecharts统计视频发布后上榜的天数
        参数：
            - video_df: 处理后的数据
            - save_filename:    保存文件名
    """
    # pandas的版本>=0.20
    video_df['diff'] = (video_df['trending_date'] - video_df['publish_date']).dt.days
    days_df = video_df['diff'].value_counts()

    # 观察视频发布后2个月的情况
    days_df = days_df[(days_df.index >= 0) & (days_df.index <= 60)]
    days_df = days_df.sort_index()
    bar = Bar('视频发布后2个月的情况')
    bar.add('柱状图', days_df.index.tolist(), days_df.values.tolist(),
            is_datazoom_show=True,  # 启用数据缩放功能
            datazoom_range=[0, 50]  # 百分比范围
            )

    line = Line()
    line.add('折线图', days_df.index.tolist(), days_df.values.tolist())

    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line)
    overlap.render(os.path.join(config.output_path, save_filename))


def plot_relationship_of_cols(all_video_df, cols):
    """
         查看列之间的关系

    """
    sel_video_df = all_video_df[cols + ['country']]

    # pair plot
    g = sns.pairplot(data=sel_video_df, hue='country')
    g.savefig(os.path.join(config.output_path, 'pair_plot.png'))
    plt.show()

    # heat map
    # 计算每两个列之间的皮尔逊相关系数
    corr_df = sel_video_df.corr()
    sns.heatmap(corr_df, annot=True)
    plt.savefig(os.path.join(config.output_path, 'heat_map.png'))
    plt.show()


def main():
    """
        主函数
    """
    all_video_df = combine_video_data()

    # 绘制每个国家指定列的的top10
    plot_top10_by_country(all_video_df, 'category', '各国的类别Top10', 'top10_category.png')
    plot_top10_by_country(all_video_df, 'channel_title', '各国的频道Top10', 'top10_channel.png')

    # 统计视频发布后上榜的天数
    plot_days_to_trend(all_video_df, 'publish_vs_trend.html')

    # 查看views,likes,dislikes,comment_count的关系
    cols = ['views', 'likes', 'dislikes', 'comment_count']
    plot_relationship_of_cols(all_video_df, cols)


if __name__ == '__main__':
    main()
