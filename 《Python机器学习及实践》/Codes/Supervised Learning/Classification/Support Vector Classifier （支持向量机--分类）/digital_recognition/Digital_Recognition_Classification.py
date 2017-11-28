# coding:utf-8

#-----------------------------手写体数据读取---------------------------

# 从 sklearn.datasets 里导入手写体数字加载器
from sklearn.datasets import load_digits
# 通过数据加载器获得手写字体的数码图像数据并存储在diagits变量中。
digits = load_digits()
print digits.data.shape     #diagits.images（1797个8*8数组）/data/target_names（0-9）/DESCR(数据集描述，如作者来源)／target（所有的结果 1797个数字）





#-----------------------------手写体数据分割---------------------------

# 使用sklearn.cross_validation里的train_test_split模块用于分割数据
from sklearn.cross_validation import train_test_split

#随机采样25%的数据用于测试，剩下的75%用于构建训练集合
x_train , x_test , y_train , y_test = train_test_split(digits.data , digits.target , test_size=0.25 , random_state= 33)

print y_train.shape
print y_test.shape




#-----------------------------训练基于线性假设的支持向量机模型---------------------------

# 从sklearn.preprocessing里导入StandardScaller     标准化数据
from sklearn.preprocessing import StandardScaler
# 从sklearn.svm里导入基于线性假设的支持向量机分类器LinearSVC
from sklearn.svm import LinearSVC

# 对训练和测试的特征数据进行标准化
ss = StandardScaler()
x_train = ss.fit_transform(x_train)
x_test = ss.transform(x_test)

# 初始化线性假设的支持向量机分类器 LinearSVC
lsvc = LinearSVC()
# 进行模型训练
lsvc.fit(x_train,y_train)
# 用训练好的模型对测试样本的数字类别进行预测，预测结果储存在变量y_predict中。
y_predict = lsvc.predict(x_test)



#-----------------------------对支持向量机分类模型从事手写体数字图像识别任务进行性能评估---------------------------

# 使用模型自带的评估函数进行准确性（Accuracy）测评
print 'The Accuracy of LinearSVC is:' , lsvc.score(x_test , y_test)

#使用sklearn.metrics 里的 Classification_report 对预测结果做进一步分析
from sklearn.metrics import classification_report
print classification_report(y_test , y_predict , target_names= digits.target_names.astype(str))



