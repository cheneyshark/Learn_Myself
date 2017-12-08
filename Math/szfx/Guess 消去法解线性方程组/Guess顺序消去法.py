# coding:utf-8

import numpy as np
import sys

# 设置矩阵
def set_matrix():
    # 设置系数矩阵A
    matrix_a =np.mat([
        [2.0, 1.0, 2.0],
        [5.0, -1.0, 1.0],
        [1.0, -3.0, -4.0]],dtype=float)
    matrix_b = np.mat([5, 8, -4],dtype=float).T
    return matrix_a, matrix_b


# 高斯顺序消去法
def gauss_shunxu(mat):
    for i in range(0,mat.shape[0]-1):
        # 判断顺序顺序主子式的首个元素不为0
        if mat[i,i] == 0:
            print mat
            print 'break:(', i, '，', i, ')元素为0'
            break
        else:
            # i行下面的每一行分别跟i行做计算，消掉第i个元素
            mat[i+1:,:] = mat[i+1:,:] - (mat[i+1:,i]/mat[i,i])*mat[i,:]
    return mat

def huidai(mat):
    x = np.mat(np.zeros(mat.shape[0],dtype=float))
    # 先算x(n)   用 b(n)/a(nn)
    n = x.shape[1]-1
    x[0,n] = mat[n,n+1]/mat[n,n]
    # 再分别带入上一部式子算出n-1
    for i in range(n):
        n -= 1
        x[0,n] = (mat[n,mat.shape[1]-1] - np.sum(np.multiply(x[0, n+1:], mat[n,n+1:mat.shape[1]-1])))/mat[n,n]
    return x


if __name__ == "__main__":
    # 增广矩阵m为系数矩阵A加上列矩阵b
    m = np.hstack(set_matrix())            #按列合并：vstack()   按行合并：hstack()
    print '原矩阵：'
    print m

    # 顺序消去过程
    m1 = gauss_shunxu(m)
    print '\n上三角矩阵：'
    print m1

    # 回带过程
    x = huidai(m1)
    print '\n\nX的值为:', x

