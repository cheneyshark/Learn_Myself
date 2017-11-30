# coding:utf-8


#--------------------------------------------------------------------------------------------
# 用随机森林模型，梯度提升决策树模型，极端随机森林模型（Extremely Randomized Trees）
# 极端随机森林在每当构建一棵树的分裂节点（nodes）的时候，不会任意地选取特征，而是先随机手机一部分特征，然后利用信息熵（Information Gain）
#     和基尼不纯性（Gini Impurity）等指标挑选最佳的节点特征。
#--------------------------------------------------------------------------------------------



#--------------------------------数据整理----------------------------------

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




# -------------------------使用三种集成回归模型对波士顿房价进行回归预测---------------------------

# 随机森林 Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor()
rfr.fit(x_train, y_train.ravel())
rft_y_predict = rfr.predict(x_test)

# 梯度提升决策树 GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor
gbr = GradientBoostingRegressor()
gbr.fit(x_train, y_train.ravel())
gbr_y_predict = gbr.predict(x_test)

# 极端随机森林 Extremely Randomized Trees
from sklearn.ensemble import ExtraTreesRegressor
etr = ExtraTreesRegressor()
etr.fit(x_train, y_train.ravel())
etr_y_predict = etr.predict(x_test)






#----------------------------------------------性能评估----------------------------------------------

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
print 'R-squared value of RandomForestRegressor is', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rft_y_predict))
print 'The mean squared error of RandomForestRegressor is', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rft_y_predict))
print 'The mean absolute error of RandomForestRegressor is', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rft_y_predict))
print''
print 'R-squared value of GradientBoostingRegressor is', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(gbr_y_predict))
print 'The mean squared error of GradientBoostingRegressor is', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(gbr_y_predict))
print 'The mean absolute error of GradientBoostingRegressor is', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(gbr_y_predict))
print''
print 'R-squared value of ExtraTreesRegressor is', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(etr_y_predict))
print 'The mean squared error of ExtraTreesRegressor is', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(etr_y_predict))
print 'The mean absolute error of ExtraTreesRegressor is', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(etr_y_predict))
print ''

# 利用训练好的极端回归森林模型，输出没中特征对预测目标的贡献度
import numpy as np
print np.sort(zip(etr.feature_importances_,boston.feature_names),axis=0)
