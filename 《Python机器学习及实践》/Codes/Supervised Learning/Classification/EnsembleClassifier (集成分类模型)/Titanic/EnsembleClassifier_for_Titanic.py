# coding:utf-8

# --------------------------------------------------------------------------------
# 集成（Ensemble）分类模型是综合考量多个分类器的预测结果，从而做出决策。
# 综合考量方式大体分为两种：
#  1、利用相同的训练数据同时搭建多个独立的分类模型。然后通过投票方式，以少数服从多数的原则作出最终的分类决策。
#         如随机森林分类器（Random Forest Classifier），在相同的训练数据上同时搭建多棵决策树。（决策树节点随机选取特征）
#  2、按照一定次序搭建多个分类模型。整合多个分类能力较弱的分类器，搭建出具有更强分类能力的模型。
#         如梯度提升决策树（Gradient Tree Boosting）每一棵决策树在生成的过程中都会尽可能降低整体集成模型在训练数据上的拟合误差。
# --------------------------------------------------------------------------------





import pandas as pd

# 读取泰坦尼克乘客档案。并存在变量titanic中。
titanic = pd.read_csv('http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt')

# 人工选取 pclass,age,sex 作为特征
x = titanic[['pclass','age','sex']]
y = titanic['survived']

# 对于缺失的年龄信息，我们使用全体乘客的平均年龄代替，这样可以在保证书你训练模型的同时，尽可能不影响预测任务。
x['age'].fillna(x['age'].mean(),inplace=True)

# 分割数据
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x, y, test_size=0.25, random_state=33)

# 对类别型特征进行转化，成为特征向量
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer(sparse=False)
x_train = vec.fit_transform(x_train.to_dict(orient = 'record'))
x_test = vec.transform(x_test.to_dict(orient='record'))


# 使用单一决策树进行模型训练以及预测分析
from sklearn.tree import DecisionTreeClassifier
dtc = DecisionTreeClassifier()
dtc.fit(x_train, y_train)
dtc_y_predict = dtc.predict(x_test)

# 使用随机森林分类器进行集成模型的训练以及预测分析
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()
rfc.fit(x_train, y_train)
rfc_y_predict = rfc.predict(x_test)

# 使用梯度提成决策树进行集成模型的训练以及预测分析
from sklearn.ensemble import GradientBoostingClassifier
gbc = GradientBoostingClassifier()
gbc.fit(x_train, y_train)
gbc_y_predict = gbc.predict(x_test)






#--------------------------------------性能预测------------------------------------------

from sklearn.metrics import classification_report

# 输出单一决策树在测试机上的分类准确性，以及更加详细的精确率，召回率，F1指标
print 'The accuracy of DecisionTreeClassifier is', dtc.score(x_test, y_test)
print classification_report(dtc_y_predict, y_test)

# 输出随机森林分类器的性能。
print 'The accuracy of RandomForestClassifier is', rfc.score(x_test, y_test)
print classification_report(rfc_y_predict, y_test)

# 输出梯度提升决策树的性能。
print 'The accuracy of GradientBoostingClassifier is', gbc.score(x_test, y_test)
print classification_report(gbc_y_predict, y_test)
