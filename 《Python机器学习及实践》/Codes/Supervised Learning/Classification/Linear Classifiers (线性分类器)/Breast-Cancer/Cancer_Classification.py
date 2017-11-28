# coding:utf-8

import pandas as pd
import numpy as np

#-----------------------------数据预处理---------------------------

# 创建特征列表
column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size',
                'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size',
                'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']

# 使用 pandas.read_csv函数从互联网读取指定数据
# data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data'
#                    ,names = column_names)
# 已经用download_a_file_in_url函数下载到本地目录下
data = pd.read_csv('breast-cancer-wisconsin.data', names=column_names)


# 处理数据  将？替换为标准缺失值表示
data = data.replace(to_replace='?',value=np.nan)  # 把问好的项目替换为numpy.nan值
# 丢弃带有缺失值的数据（只要有一个维度有缺失）
data = data.dropna(how = 'any')       # data用法： dropna(axis = 0(行)、1（列） ， how = 'all'(所有空才删)、'any'（任意一项为空就删））
# 输出data的数据量和维度
print '筛选后data数据的维度为：' , data.shape




#-----------------------------准备测试数据---------------------------

# 使用sklearn.cross_validation里的train_test_split模块用于分割数据
from sklearn.cross_validation import train_test_split

#随机采样25%的数据用于测试，剩下的75%用于构建训练集合
x_train , x_test , y_train , y_test = train_test_split(data[column_names[1:10]],data[column_names[10]],
                                                       test_size=0.25,random_state=33)   #用法见最下（train_test_split）

# 查验训练样本、测试样本的数量和类别分布
print y_train.value_counts()
print y_test.value_counts()





#-----------------------------使用线性分类模型从事良／恶性肿瘤预测任务---------------------------
# 使用逻辑斯蒂回归与随机梯度参数估计两种方法对处理后的训练数据进行学习

# 从sklearn.preprocessing里导入StandardScaller     标准化数据
from sklearn.preprocessing import StandardScaler
# 从sklearn.linear_model里导入LogisticRegression 与 SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

# 标准化数据，保证每个维度的特征数据方差为1，均值为0。使得预测结果不会被某些维度过大的特征值而主导。
ss = StandardScaler()
x_train = ss.fit_transform(x_train)                 #原因见最下（标准化数据）
x_test = ss.transform(x_test)


# 初始化 LogisticRegression 与 SGDClassfier
lr = LogisticRegression()
sgdc = SGDClassifier()

# 调用 LogisticRegression 中的fit函数用来训练模型参数。
lr.fit(x_train, y_train)
# 使用训练好的模型lr对x_test进行预测，结果储存在变量lr_y_predict中。
lr_y_predict = lr.predict(x_test)

# 调用SGDClassifier 中的fit函数用来训练模型参数。
sgdc.fit(x_train, y_train)
# 使用训练好的模型sgdc对x_test进行预测，结果储存在变量sgdc_y_predict中。
sgdc_y_predict = sgdc.predict(x_test)









#-----------------------------使用线性分类模型从事良／恶性肿瘤预测任务的性能分析---------------------------

# 从sklearn.metrics里导入classification_report模块。
from sklearn.metrics import classification_report

# 使用逻辑斯蒂回归模型自带的评分函数score获得模型在测试集上的准确性结果。
print 'Accuracy of LR Classifier:', lr.score(x_test,y_test)
# 利用classification_report模块获得LogisticRegression其他三个指标的结果。
print classification_report(y_test, lr_y_predict, target_names=['Benign','Malignant'])  #缺省的target_names就显示为labels，为2，4  具体用法见下：分类报告

# 使用随机梯度下降模型自带的评分函数score获得模型在测试集上的准确性结果
print 'Accuracy of SGD Classifier:', sgdc.score(x_test,y_test)
# 利用classification_report模块获得SGDClassifier其他三个指标的结果.
print classification_report(y_test, sgdc_y_predict, target_names=['Benign','Malignant'])

















#-----------------------------标准化数据---------------------------
# 原因：比如第一个维度的特征是1-10，而第二个维度的特征是10000-20000，如果直接进行计算第二个维度的特征明显占据主导位置，
#          导致第一个维度被忽略，因此要将所有维度全部标准化，对所有维度进行统一处理，保证各维度间的标准一致。
#               处理公式：x' = (x - 均值 ）／标准差
#       之所以训练数据先fit在transform是因为：
#             fit_transform(partData)对部分数据先拟合fit，找到该part的整体指标，如均值、方差、最大值最小值等等（根据具体转换的目的），
#               然后对该partData进行转换transform，从而实现数据的标准化、归一化等等。。
#             根据对之前部分fit的整体指标，对剩余的数据（restData）使用同样的均值、方差、最大最小值等指标进行转换transform(restData)，
#               从而保证part、rest处理方式相同。
#             必须先用fit_transform(partData)，之后再transform(restData)
#             如果直接transform(partData)，程序会报错
#             如果fit_transfrom(partData)后，使用fit_transform(restData)而不用transform(restData)，虽然也能归一化，但是两个结果不是
#                                                                                           在同一个“标准”下的，具有明显差异。





#-----------------------------train_test_split---------------------------
# X_train,X_test, y_train, y_test =cross_validation.train_test_split(train_data,train_target,test_size=0.4, random_state=0)
# 参数解释：
# train_data：所要划分的样本特征集
# train_target：所要划分的样本结果
# test_size：样本占比，如果是整数的话就是样本的数量
# random_state：是随机数的种子。
# 随机数种子：其实就是该组随机数的编号，在需要重复试验的时候，保证得到一组一样的随机数。比如你每次都填1，其他参数一样的情况下你得到的随机数组是一样的。但填0或不填，每次都会不一样。
#
#



#-----------------------------classification_report 分类报告---------------------------
# 分类报告：sklearn.metrics.classification_report(y_true, y_pred, labels=None, target_names=None,sample_weight=None, digits=2)，
#           显示主要的分类指标，返回每个类标签的精确、召回率及F1值
# 主要参数说明：
# labels：分类报告中显示的类标签的索引列表 (及最终结果的类别值，如此代码中，labels的值缺省为2、4)
# target_names：显示与labels对应的名称
# digits：指定输出格式的精确度
# 精度(precision) = 正确预测的个数(TP)/被预测正确的个数(TP+FP)
# 召回率(recall)=正确预测的个数(TP)/预测个数(TP+FN)
# F1 = 2*精度*召回率/(精度+召回率)
# support 各指标的加权平均值