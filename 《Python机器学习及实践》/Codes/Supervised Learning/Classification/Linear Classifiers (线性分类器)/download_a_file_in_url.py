# coding: utf-8


import urllib
import os

# 显示下载进度的方法
def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print '%.2f%%' % per

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data'
#local = url.split('/')[-1]
local = os.path.join('../','breast-cancer-wisconsin.data')


urllib.urlretrieve(url,local,Schedule)