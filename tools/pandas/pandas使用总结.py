# coding:utf-8

import pandas as pd

# 一、导入和保存数据
#   导入数据
data = pd.read_csv('titanic.txt')
#   写入CSV文件
# data.to_csv('write_test.csv')


#二、查看数据
#   查看数据类型
# print data.dtypes

#   查看头部和尾部   （括号中的数字可以表示头尾行数，缺省为5行）
# print data.head(3)
# print data.tail(4)

#   查看索引、列、底层数据
# print data.index
# print data.columns    (print data.columns.values)
# print data.values

#   快速统计汇总
# print data.describe()     # percent:百分位数  eg:percent = [.25,.50,.75]  include:dtype类型的列表 eg:include=['O']
# print data.info()
# print data.shape

#   对pandas进行转置
# data.T


#三、 排序   sort
#   columns:要排序的列名称     ascending: True为升序    False为降序    axis： 0  行排列   1 列排列
#   inplace: True 更改原数据  不创建新实例     na_position： 'first' 'last'  控制放在位置
# print data.sort_values(['age'],ascending=False).head(10)



#四、筛选
#   筛选某列特定值
# print data.loc[data['age']==71,['name','age','pclass']].head()
# print data.loc[(data['age'] >= 70) | (data['age']==7), ['name','age']]

#   筛选某些行
# print data[0:1]
# print data.loc[0:3,['name','age']]
# print data[data['age'] > 60]
# print data[data['age'].isin([50,71])]

#   通过位置进行选择
# print data.iloc[3:5,0:2]


#五、缺失值处理
#   去掉包含缺失值的行
# data.dropna(how='any')
#   去掉所有值为NaN的行
# data.dropna(how='all')

#   填充缺失值
# print data.fillna('WWWWW')
# 可使用字典序对不同的列做不同处理
# print data.fillna({'age':123,'room':'WWWWWWWWWW'})

# 用fillna方法填充 NA 处的值    inplace参数缺省为 false 设置为True更改原数组
# x['age'].fillna(x['age'].mean() , inplace = True)
# data.fillna(data.mean()['age','room'])


#六、分组 groupby
#   groupby中by参数用来对数据分组，分组后格式为groupby类型，可以通过.size（）方法返回个数
# print data[['pclass','survived']].groupby(by=['pclass'],as_index=False).size()
print data[['pclass','survived']].groupby(by='pclass',as_index=False).mean()


#七、统计
#   按照年龄参数，统计各个值出现的概率
# print data['age'].value_counts()