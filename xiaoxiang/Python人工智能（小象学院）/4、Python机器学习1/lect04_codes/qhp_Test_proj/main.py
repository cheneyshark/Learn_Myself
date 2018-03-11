# coding: utf-8

"""
    作者:     qhp
    版本:     1.0
    日期:     2018/03
    文件名:    main.py
    功能：     主程序

    任务：使用scikit-learn建立不同的机器学习模型进行手机价格等级预测

"""

import os
import config
import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from matplotlib.font_manager import FontProperties

np.set_printoptions(suppress=True)

def get_font():
    """
    解决mac环境下 plot不能显示中文问题
    :return: --fontproperties--
    """
    fontproperties = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

    return fontproperties


def inspect_dataset(train_data, test_data):
    """
    观测数据
    :param train_data: 训练集
    :param test_data: 测试集
    :return:
    """
    print('\n===================== 数据查看 =====================')
    print('训练集有{}条记录。'.format(len(train_data)))
    print('测试集有{}条记录。'.format(len(test_data)))

    # 通过可视化查看测试集和训练集的价格区间
    plt.figure(figsize=(10, 5))
    ax1 = plt.subplot(1, 2, 1)
    sns.countplot(x=config.label_col, data=train_data)
    plt.title('训练集数据', fontproperties=get_font())
    plt.xlabel('价格等级', fontproperties=get_font())
    plt.ylabel('数量', fontproperties=get_font())

    plt.subplot(1, 2, 2, sharey=ax1)
    plt.title('测试集数据', fontproperties=get_font())
    sns.countplot(x=config.label_col, data=test_data)
    plt.xlabel('价格等级', fontproperties=get_font())
    plt.ylabel('数量', fontproperties=get_font())

    plt.tight_layout()
    plt.show()



def main():
    """
    主函数
    :return:
    """
    # 加载数据
    undressed_data = pd.read_csv(os.path.join(config.dataset_path, 'data.csv'))
    train_data, test_data = train_test_split(undressed_data, test_size=0.25, random_state=77)

    # 数据查看
    # inspect_datasetfeat_cols(train_data, test_data)

    # 构建数据集
    X_train = train_data[config.feat_cols].values
    X_test = test_data[config.feat_cols].values
    y_train = train_data[config.label_col].values
    y_test = test_data[config.label_col].values

  


if __name__ == '__main__':
    main()