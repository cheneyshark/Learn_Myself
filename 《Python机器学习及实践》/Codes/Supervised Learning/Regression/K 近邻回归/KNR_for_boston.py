# coding: utf-8

# ---------------------------------------------------------------------------------
# K近邻回归模型只是借助周围 K 个最近训练样本的目标数值，对待测样本的回归值进行决策。
# 有多种不同配置的K近邻模型  取决目标数值是使用普通算术平均还是考虑距离差异进行加权平均
# ---------------------------------------------------------------------------------



#-----------------------------数据准备---------------------------

from sklearn.datasets import load_boston
boston = load_boston()

x = boston.data
y = boston.target

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=33)

# 标准化数据
from sklearn.preprocessing import StandardScaler
ss_x = StandardScaler()
ss_y = StandardScaler()
x_train = ss_x.fit_transform(x_train)
x_test = ss_x.transform(x_test)
y_train = ss_y.fit_transform(y_train.reshape(-1,1))
y_test = ss_y.transform(y_test.reshape(-1,1))



#-----------------------------使用两种不同配置的K近邻回归模型对美国波士顿房价数据进行回归预测---------------------------

# 从 sklearn.neighbors 导入 KNeighborRegressor （K近邻回归器）
from sklearn.neighbors import KNeighborsRegressor

# 初始化K近邻回归器，并且调整配置，使得预测的方式为平均回归： weights = 'uniform'
uni_knr = KNeighborsRegressor(weights='uniform')
uni_knr.fit(x_train,y_train.ravel())
uni_knr_y_predict = uni_knr.predict(x_test)

# 初始化K近邻回归器，并且调整配置，使得预测的方式为根据距离加权回归： weights = 'distance'
dis_knr = KNeighborsRegressor(weights='distance')
dis_knr.fit(x_train, y_train.ravel())
dis_knr_y_predict = dis_knr.predict(x_test)



#-----------------------------性能评估---------------------------

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

print 'R-squared value of uniform-weighted KNeighborRegressor', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(uni_knr_y_predict))
print 'The mean squared error of uniform-weighted KNeighborRegressor', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(uni_knr_y_predict))
print 'The mean absolute error of uniform-weighted KNeighborRegressor', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(uni_knr_y_predict))
print ''

print 'R-squared value of distance-weighted KNeighborRegressor', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(dis_knr_y_predict))
print 'The mean squared error of distance-weighted KNeighborRegressor', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(dis_knr_y_predict))
print 'The mean absolute error of distance-weighted KNeighborRegressor', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(dis_knr_y_predict))
