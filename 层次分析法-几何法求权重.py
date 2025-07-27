import numpy as np

#定义判断矩阵A
A=np.array([[1,2,3,5],[1/2,1,1/2,2],[1/3,2,1,2],[1/5,1/2,1/2,1]])

#获取A的行和列
n=A.shape[0]

#将A中每一行元素相乘得到一列向量
#np.power函数可以计算一维数组中所有元素的乘积
#还可以通过指定axis参数来计算多维数组的某个维度上的元素的乘积。
#例如，在二维数组中,axis=0表示按列计算乘积,axis=1，表示按行计算乘积
prod_A=np.prod(A,axis=1)

#将新的向量的每个分量开n次方等价求1/n次方
#np.power是Numpy库中的一个函数,用于数组中的元素进行幂运算
prod_n_A=np.power(prod_A,1/n)

#归一化处理
re_prod_A=prod_n_A/np.sum(prod_n_A)

#展示权重结果
print(re_prod_A)