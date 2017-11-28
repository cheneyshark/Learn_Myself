
#coding:utf-8


import pandas as pd

# 用pandas的read_csv函数将train、test的表格参数导出
df_train = pd.read_csv('../Breast-Cancer/breast-cancer-train.csv')
df_test = pd.read_csv('../Breast-Cancer/breast-cancer-test.csv')

# 选取'Clump Thickness' 与 'Cell Size' 为特征，构建测试集中的正负分类样本(以Type的值进行分类)。
df_test_negative = df_test.loc[df_test['Type']==0][['Clump Thickness','Cell Size']]
df_test_positive = df_test.loc[df_test['Type']==1][['Clump Thickness','Cell Size']]

import matplotlib.pyplot as plt

# 用plt分别画出良性肿瘤样本（Type==0）及恶性肿瘤样本（Type==1）
plt.scatter(df_test_negative['Clump Thickness'],df_test_negative['Cell Size'],s=200,marker='o',c='red')
plt.scatter(df_test_positive['Clump Thickness'],df_test_positive['Cell Size'],s=150,marker='x',c='black')
plt.xlabel('Clump Thickness')
plt.ylabel('Cell Size')
# plt.show()

import numpy as np

# 利用numpy中的random函数随机采样直线的截距和系和截距
    # 截距
intercept = np.random.random([1])     # 构造n（1）个随机数 范围(0,1)  构成一个数组
    # 系数
coef = np.random.random([2])
lx = np.arange(0,12)                # lx为0 到 11 共12 个整数的数组
ly = (-intercept - lx * coef[0])/ coef[1]
# plt.plot(lx,ly,c='yellow')
# 画出书上的图1-3
# plt.show()


# 导入 sklearn 中的逻辑斯蒂回归分类器
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()

# 使用所有训练样本学习直线的系数和截距
lr.fit(df_train[['Clump Thickness','Cell Size']],df_train['Type'])
print 'Tresting accuracy (10 training samples):', lr.score(df_test[['Clump Thickness','Cell Size']],df_test['Type'])
# 将回归后的系数和截距赋值并构造新函数
intercept = lr.intercept_
coef = lr.coef_[0,:]    #lr.coef_返回的是一个多维Tuple  取第一个数组
# print lr.coef_

# 原本这个分类面为 lx * coef[0] + ly * coef[1] + intercept = 0,映射到2维平面，为：
ly = (-intercept - lx * coef[0])/ coef[1]

# 画图
plt.plot(lx,ly,c='green')
plt.show()
