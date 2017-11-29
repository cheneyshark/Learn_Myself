# coding:utf-8

#---------------------------------------------------------------------
# 此代码用SVR 支持向量机回归模型  回归波士顿房价
# 前期具体数据准备可参考线性回归器中的代码
#---------------------------------------------------------------------



#-----------------------------数据准备---------------------------

# 导入波士顿房价数据
from sklearn.datasets import load_boston
boston = load_boston()

# 数据分割
from sklearn.model_selection import train_test_split
x = boston.data
y = boston.target
x_train,x_test,y_train,y_test = train_test_split(x, y, test_size=0.25, random_state=33)

# 标准化处理
from sklearn.preprocessing import StandardScaler
ss_x = StandardScaler()
ss_y = StandardScaler()
x_train = ss_x.fit_transform(x_train)
x_test = ss_x.transform(x_test)
y_train = ss_y.fit_transform(y_train.reshape(-1,1))
y_test = ss_y.transform(y_test.reshape(-1,1))






#-----------------------------使用三种不同核函数的支持向量机回归模型进行训练，并且分别对测试数据作出预测---------------------------

# 从 sklearn.svm 中导入支持向量机（回归）模型
from sklearn.svm import SVR

# 使用线性核函数配置的支持向量机进行回归训练， 并且对测试样本进行预测。
linear_svr = SVR(kernel = 'linear')
linear_svr.fit(x_train, y_train.ravel())
linear_svr_y_predict = linear_svr.predict(x_test)


# 使用多项式核函数配置的支持向量机进行回归训练，并且对测试样本进行预测。
poly_svr = SVR(kernel='poly')
poly_svr.fit(x_train, y_train.ravel())
poly_svr_y_predict = poly_svr.predict(x_test)


# 使用径向基核函数配置的支持向量机进行回归训练，并且对测试样本进行预测。
rbf_svr = SVR(kernel='rbf')
rbf_svr.fit(x_train,y_train.ravel())
rbf_svr_y_predict = rbf_svr.predict(x_test)






#-----------------------------对三种核函数配置下的支持向量机回归模型在相同测试集上进行性能评估---------------------------

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
print 'R-squared value of linear SVR is', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(linear_svr_y_predict))
print 'The mean squared error of linear SVR is', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(linear_svr_y_predict))
print 'THe mean absolute error of linear SVR is', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(linear_svr_y_predict))
print ''

print 'R-squared value of poly SVR is', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(poly_svr_y_predict))
print 'The mean squared error of poly SVR is', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(poly_svr_y_predict))
print 'THe mean absolute error of poly SVR is', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(poly_svr_y_predict))
print ''

print 'R-squared value of rbf SVR is', r2_score(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict))
print 'The mean squared error of rbf SVR is', mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict))
print 'THe mean absolute error of rbf SVR is', mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(rbf_svr_y_predict))
