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

url = 'http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt'
#local = url.split('/')[-1]
local = os.path.join('../','titanic.txt')


urllib.urlretrieve(url,local,Schedule)