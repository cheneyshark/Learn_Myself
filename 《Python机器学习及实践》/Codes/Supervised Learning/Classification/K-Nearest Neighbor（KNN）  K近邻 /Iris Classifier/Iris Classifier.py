# coding:utf-8


#-----------------------------读取 Iris 数据集细节资料---------------------------

# 从 sklearn.datasets 里导入 iris 数据加载器。
from sklearn.datasets import load_iris
# 使用加载器读取数据并且存入变量iris。
iris = load_iris()                                      # 具体用法见下  Iris
print iris.data.shape
# 查看数据说明
print iris.DESCR





#-----------------------------对 Iris 数据集进行分割---------------------------

from sklearn.cross_validation import train_test_split
x_train , x_test , y_train , y_test = train_test_split(iris.data , iris.target , test_size=0.25 , random_state=33)
print x_train.shape
print x_test.shape





#-----------------------------使用K近邻分类器对 Iris 数据进行类别预测---------------------------

# 从 sklearn.preprocessing 里导入数据标准化模块
from sklearn.preprocessing import StandardScaler
# 从 sklearn.neighbors 里选择导入 KNeighborsClassifier， 即K近邻分类。
from sklearn.neighbors import KNeighborsClassifier

# 对训练和测试数据的特征进行标准化
ss = StandardScaler()
x_train = ss.fit_transform(x_train)
x_test = ss.transform(x_test)

# 使用K近邻分类器对测试数据进行类别预测，预测结果储存在变量y_predict中。
knc = KNeighborsClassifier()
knc.fit(x_train , y_train)
y_predict = knc.predict(x_test)




#-----------------------------对K近邻分类器在Iris数据上的预测性能进行评估---------------------------

# 使用模型自带的评估函数进行准确性测评。
print 'The accuracy of K-Nearest Neighbor Classifier is ', knc.score(x_test , y_test)

from sklearn.metrics import classification_report
print classification_report(y_test , y_predict , target_names= iris.target_names)













# -----------------------------Iris---------------------------
# iris中文指鸢尾植物，这里存储了其萼片和花瓣的长宽，一共4个属性，鸢尾植物又分三类。与之相对，iris里有两个属性iris.data，iris.target，
#   data里是一个矩阵，每一列代表了萼片或花瓣的长宽，一共4列，每一列代表某个被测量的鸢尾植物，一共采样了150条记录，所以查看这个矩阵的形状
#   iris.data.shape   共150个样本，每个样本含有四个属性值。
# target是一个数组，存储了data中每条记录属于哪一类鸢尾植物，所以数组的长度是150，数组元素的值因为共有3类鸢尾植物，所以不同值只有3个。
# iris.target_names 表示了三种类别  分别为 'setosa' 'versicolor' 'virginica'
#
# return Bunch(data=data, target=target,
#                  target_names=target_names,
#                  DESCR=fdescr,
#                  feature_names=['sepal length (cm)', 'sepal width (cm)',
#                                 'petal length (cm)', 'petal width (cm)'])