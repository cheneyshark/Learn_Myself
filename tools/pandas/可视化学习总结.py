# coding:utf-8

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



#一、线图
#Series对象
# # print np.random.randn(10)   # 从标准正态分布【0，1】返回多个样本值
# # print np.random.randn(10).cumsum()     cumsum  累加值
# s = pd.Series(np.random.randn(10).cumsum(),index=np.arange(0,100,10))
# # 缺省情况下，Series的index值被当作x轴。   可以通过 use_index=False来禁止
# # 参数： label 用于图例的标签
# #       ax  要在其上进行绘画的对象
# #       style   绘图风格（如 'ko-'）
# #       alpha   图表的不透明度（0-1）
# #       kind    'line'/'bar'/'barh'/'ked'
# #       use_index   将对象的索引用做刻度标签
# #       xticks  用作X轴刻度的值
# #       yticks      Y
# #       xlim    X轴的界限
# #       ylim
# #       grid    显示网格线   缺省为False，不显示网格
# fig = plt.figure()
# ax1 = fig.add_subplot(2,2,1)
# ax2 = fig.add_subplot(2,1,2)
# s.plot(grid=True,xticks=[1,2,3,4,5,6,7],use_index=False,kind='bar',ax=ax2)
# plt.show()


