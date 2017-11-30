# coding: utf-8

# ---------------------------------------------------------------------------------
#
# 用回归树预测波士顿房价。
#
# ---------------------------------------------------------------------------------




#-----------------------------数据准备---------------------------

from sklearn.datasets import load_boston
boston = load_boston()
x = boston.data
y = boston.target

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=33)

from sklearn.preprocessing import StandardScaler
ss_x = StandardScaler()
ss_y = StandardScaler()

x_train = ss_x.fit_transform(x_train)
x_test = ss_x.transform(x_test)
y_train = ss_y.fit_transform(y_train.reshape(-1,1))
y_test = ss_y.transform(y_test.reshape(-1,1))





#-----------------------------使用回归树对美国波士顿房价训练数据进行学习，并对测试数据进行预测---------------------------

# 从 sklearn.tree 中导入 DecisionTreeRegressor
from sklearn.tree import DecisionTreeRegressor
dtr = DecisionTreeRegressor()
dtr.fit(x_train, y_train.ravel())
dtr_y_predict = dtr.predict(x_test)








#-----------------------------对但一回归树模型在美国波士顿房价测试数据上的预测性能进行评估---------------------------

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
print 'R-squared value of DecisionTreeRegressor', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(dtr_y_predict))
print 'The mean squared error of DecisionTreeGreesor', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(dtr_y_predict))
print 'The mean absolute error of DecisionTreeGreesor', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(dtr_y_predict))