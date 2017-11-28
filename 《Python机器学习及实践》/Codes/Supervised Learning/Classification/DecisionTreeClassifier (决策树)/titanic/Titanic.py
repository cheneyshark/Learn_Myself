# coding:utf-8

#-----------------------------泰坦尼克号乘客数据查验---------------------------

# 利用 pandas 的 read_csv 模块直接读取泰坦尼克号乘客数据
import pandas as pd
titanic = pd.read_csv('../titanic.txt')
# print titanic.head()

# 使用 pandas, 数据都转入 pandas 独有的 dataframe 格式（二维数据表格），直接使用info（），查看数据的统计特性。
print titanic.info()





#-----------------------------使用决策树模型预测泰坦尼克号乘客的生还情况---------------------------

# 机器学习有一个十分重要的环节————特征的选择。 （根据我们对这场事故的了解，sex、age、pclass这些特征有可能是决定幸免与否的关键）
x = titanic[['pclass' , 'age' , 'sex']]
y = titanic['survived']
# print x.info()

# 根据输出结果，发现age列只有633个数据，其他的需要补充完整。 补充age里的数据，使用平均数或者中位数都是对模型偏离造成最早影响的策略。
x['age'].fillna(x['age'].mean() , inplace = True)   # 用fillna方法填充 NA 处的值    inplace参数缺省为 false 设置为True更改原数组
print x.info()


#  数据分割
from sklearn.model_selection import train_test_split
x_train , x_test , y_train , y_test = train_test_split(x, y, test_size=0.25 , random_state=33)

# 使用scikit-learn.feature_extraction中的特征转换器。
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer(sparse=False)          # sparse 为稀疏矩阵相关参数  具体功能不详

# 转换特征后，发现凡事类别型的特征都单独剥离出来，独成一列特征，数值型的则保持不变。
x_train = vec.fit_transform(x_train.to_dict(orient = 'record'))
print vec.feature_names_

# 同时对测试数据的特征进行转化
x_test = vec.transform(x_test.to_dict(orient = 'record'))

# 从 sklearn.tree 中导入决策树分类器
from sklearn.tree import DecisionTreeClassifier
# 使用默认配置初始化决策树分类器
dtc = DecisionTreeClassifier()
# 使用训练数据进行模型学习
dtc.fit(x_train,y_train)
# 用训练好的决策树模型对测试特征数据进行预测
y_predict = dtc.predict(x_test)




#-----------------------------决策树模型对泰坦尼克号乘客是否生还的预测性能---------------------------

# 输出预测准确值
print 'Accuracy:' , dtc.score(x_test, y_test)

# 用classification_report输出更加详细的分类性能。
from sklearn.metrics import classification_report
print classification_report(y_test, y_predict, target_names=['died' , 'survived'])
