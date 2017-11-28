# coding:utf-8

#-----------------------------读取20类新闻文本的数据细节---------------------------

# 从 sklearn.datasets 里导入新闻数据抓取器 fetch_20newsgroups
from sklearn.datasets import fetch_20newsgroups
news = fetch_20newsgroups(subset='all')             # 详细用法见下 fetch_20newsgroups

print len(news.data)
print news.target_names
# print news.data[18845]





#-----------------------------20类新闻文本数据分割---------------------------

# 从 sklearn.cross_validation 导入 train_test_split。
from sklearn.cross_validation import train_test_split
x_train , x_test , y_train , y_test = train_test_split(news.data , news.target , test_size=0.25 , random_state=33)





#-----------------------------使用朴素贝叶斯对新闻文本数据进行类别预测---------------------------

# 从 sklearn.feature_extraction.text 里导入用于文本特征向量转化模块。
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer()
x_train = vec.fit_transform(x_train)
x_test = vec.transform(x_test)

# 从 sklearn.naive_bayes 里导入朴素贝叶斯模型
from sklearn.naive_bayes import MultinomialNB
# 初始化模型
mnb = MultinomialNB()
# 利用训练数据对模型进行估计
mnb.fit(x_train , y_train)
# 对测试样本进行类别预测。
y_predict = mnb.predict(x_test)






#-----------------------------对朴素贝叶斯分类器在新闻文本数据上的表现性能进行评估---------------------------

# 从sklearn.metrics里导入classification_report模块。
from sklearn.metrics import classification_report

print 'The Accuracy of Naive Bayes Classifier is:' , mnb.score(x_test,y_test)
print classification_report(y_test , y_predict , target_names=news.target_names)























#-----------------------------fetch_20newsgroups---------------------------
# ##函数原型是这样的。
# '''
# fetch_20newsgroups(data_home=None,subset='train',categories=None,shuffle=True,random_state=42,remove=(),download_if_missing=True)
# '''
# '''
# data_home指的是数据集的地址，如果默认的话，所有的数据都会在'~/scikit_learn_data'文件夹下.
#
# subset就是train,test,all三种可选，分别对应训练集、测试集和所有样本。
#
# categories:是指类别，如果指定类别，就会只提取出目标类，如果是默认，则是提取所有类别出来。
#
# shuffle:是否打乱样本顺序，如果是相互独立的话。
#
# random_state:打乱顺序的随机种子
#
# remove:是一个元组，用来去除一些停用词的，例如标题引用之类的。
#
# download_if_missing: 如果数据缺失，是否去下载。
#
# twenty_train.data是一个list类型，每一个元素是str类型，也就是一篇文章。
# twenty_train.target则是它的标签。