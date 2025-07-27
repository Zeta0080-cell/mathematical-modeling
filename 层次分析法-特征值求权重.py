import numpy as np

#定义判断矩阵A
A=np.array([[1,2,3,5],[1/2,1,1/2,2],[1/3,2,1,2],[1/5,1/2,1/2,1]])

#获取A的行和列
n=A.shape[0]

#求出特征值和特征向量
eig_values,eig_vectors=np.linalg.eig(A)

#找出最大特征值的索引,np.argmax是Numpy库中的一个函数，用于返回数组中的最大索引值
max_index=np.argmax(eig_values)

#找出对应的特征向量
max_vector=eig_vectors[:,max_index]

#对特向量进行归一化处理,得到权重
weights=max_vector/np.sum(max_vector)

#输出权重
print(weights)