# coding: utf-8

from sklearn import datasets

iris = datasets.load_iris()
# 数据集描述信息
iris.DESCR
# iris数据集的数据
iris.data
# 以上总共150组数据，对应以下150个结果
iris.target
# 0代表Setosa  1代表Versicolour   2代表 Virginica
iris.target_names
# 绘制散点图
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn import datasets

# 加载iris数据集
iris = datasets.load_iris()
# 取出iris数据中的第2列，即表示花瓣长度
x = iris.data[:, 0]  # x轴
y = iris.data[:, 3]  # y轴   花瓣宽度
x
y
species = iris.target  # 种类
# 计算散点图x轴最小值，最大值
x_min, x_max = x.min() - .5, x.max() + .5
# 计算散点图y轴最小值与最大值
y_min, y_max = y.min() - .5, y.max() + .5
# 以下绘制散点图
plt.figure()

# matplot显示图例中的中文问题 :   https://www.zhihu.com/question/25404709/answer/67672003
import matplotlib.font_manager as fm

# mac中的字体问题请看: https://zhidao.baidu.com/question/161361596.html
myfont = fm.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

# 图例中的中文处理
plt.legend(prop=myfont)

plt.title(u'鸢尾花分类预测_根据花瓣长宽', fontproperties=myfont)
plt.scatter(x, y, c=species)
plt.xlabel(u'花瓣长 Petal length', fontproperties=myfont)
plt.ylabel(u'花瓣宽 Petal width', fontproperties=myfont)

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.plot()

# 将图表保存为png图片, 注意这句话必须在plot()之后，否则将得到一个空白图片
plt.savefig('python_8_2_鸢尾花分类预测_根据花瓣长宽.png')

plt.show()
# shift+enter显示图表