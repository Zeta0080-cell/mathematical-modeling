import numpy as np

def round_decimal(A, n):
    for i in np.arange(A.shape[0]):
        for j in np.arange(A.shape[1]):
            a = A[i,j]
            b = int(a * 10**n) * 10**(-n)  # 截断到n位小数
            # 四舍五入判断
            if a - b >= 0.5 * 10**(-n):
                b = b + 10**(-n)
            A[i,j] = b
    return A