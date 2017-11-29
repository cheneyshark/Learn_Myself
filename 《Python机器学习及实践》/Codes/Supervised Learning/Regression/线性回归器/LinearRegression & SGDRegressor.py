# coding:utf-8

#-----------------------------导入波士顿房价数据---------------------------

# 从 sklearn.datasets 里导入波士顿房价数据读取器
from sklearn.datasets import load_boston
boston = load_boston()
# print boston.DESCR                   #('data', the data to learn, 'target', the regression targets,and
                                        # 'DESCR', the full description of the dataset.)


#-----------------------------数据分割---------------------------

from sklearn.model_selection import train_test_split

# 导入 numpy 并重命名为 np.      (用于后期分析回归目标值的差异)
import numpy as np

x = boston.data
y = boston.target

# 随机采样25%的数据构建测试样本，其余作为训练样本
x_train , x_test , y_train , y_test = train_test_split(x , y ,test_size=0.25 , random_state=33)

# 分析回归目标值的差异
print 'The max target value is' , np.max(y)
print 'The min target value is' , np.min(y)
print 'The avarage target value is' , np.mean(y)




#-----------------------------数据标准化---------------------------

from sklearn.preprocessing import StandardScaler
ss_x = StandardScaler()
ss_y = StandardScaler()

x_train = ss_x.fit_transform(x_train)
x_test = ss_x.transform(x_test)
y_train = ss_y.fit_transform(y_train.reshape(-1,1))
y_test = ss_y.transform(y_test.reshape(-1,1))



#-----------------------------使用线性回归模型LinearRegression和随机梯度下降回归模型（SGDRegression）分别进行预测---------------------------

# LinearRegression
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(x_train , y_train)
lr_y_predict = lr.predict(x_test)


# SGD Regression
from sklearn.linear_model import SGDRegressor
sgdr = SGDRegressor(max_iter=1000)                      #   最大迭代次数设置
sgdr.fit(x_train , y_train.ravel())                     # 把二维数组转换为1维数组  对应上面的y_train_reshape(-1,1)
sgdr_y_predict = sgdr.predict(x_test)



#-----------------------------使用三种回归评价机制以及两种调用R-squared评价模块的方法，对本届模型的回归性能作出评价---------------------------

# 使用 LinearRegression 自带的评估模块，并输出评价结果。
print 'The value of default measurement of LinearRegression is', lr.score(x_test , y_test)

# 从 sklearn.metrics 依次导入 r2_score、 mean_squared_error、mean_absolute_error 用于回归性能的评估
from sklearn.metrics import r2_score , mean_squared_error , mean_absolute_error

# 使用 r2_score 模块，并输出评估结果
print 'The value of R-squared of LinearRegression is', r2_score(y_test , lr_y_predict)

# 使用 mean_squared_error 模块，并输出评估结果。
print 'The mean squared error of LinearRegression is', mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(lr_y_predict))

# 使用 mean_absolute_error 模块，并输出评估结果。
print 'The mean absolute error of LinearRegression is', mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(lr_y_predict))









# 使用 SGDRegressor 模型自带的评估模块，并输出评估结果。
print 'The value of default measurement of SGDRegressor is', sgdr.score(x_test , y_test)

# 使用 r2_score 模块，并输出评估结果
print 'The value of R-squared of SGDRegressor is', r2_score(y_test, sgdr_y_predict)

# 使用 mean_squared_error 模块，并输出评估结果。
print 'The mean squared error of SGDRegressor is', mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(sgdr_y_predict))

# 使用 mean_absolute_error 模块，并输出评估结果。
print 'The mean absolute error of SGDRegressor is', mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(sgdr_y_predict))



