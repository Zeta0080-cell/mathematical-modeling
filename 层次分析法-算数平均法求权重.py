import numpy as np

#定义判断矩阵A
A=np.array([[1,2,3,5],[1/2,1,1/2,2],[1/3,2,1,2],[1/5,1/2,1/2,1]])

#计算每列的和
#np.sum函数可以计算以为数组中所有元素的和
#还可以通过指定axis参数来计算多维数组的某个维度上的元素总和。例如,在二维数组中,axis=0表示按列计算总和,axis=1表示按行计算总和。
ASum=np.sum(A,axis=0)

#获取A的行和列
n=A.shape[0]

#归一化,二维数组除以一位数组,会自动将一维数组扩展为与二维数组相同的形状,然后进行逐元素的除法运算
Stand_A=A/ASum

#各列相加到同一行
ASumr=np.sum(Stand_A,axis=1)

#计算权重向量
weights=ASumr/n

print(weights)
