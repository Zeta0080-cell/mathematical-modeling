import numpy as np
from function import f3  # 用于计算螺线上的位置迭代
from zeropoint import zero2  # 用于计算函数f3的零点


def judge(theta, d, v0):
    d1 = 0.275  # 内侧距离阈值
    d2 = 0.15  # 外侧距离阈值
    let_theta = [theta]

    # 第一部分：计算角度轨迹
    for i in np.arange(223):
        if i == 0:
            d0 = 3.41 - 0.275 + 2
        else:
            d0 = 2.2 - 0.275 + 2

        theta_last = let_theta[-1]  # 获取上一个角度值
        a = theta_last
        b = theta_last + np.pi / 2
        theta_new = zero2(f3, a, b, 1e-9, d, d0, theta_last)
        let_theta.append(theta_new)

        if theta_new - theta > 3 * np.pi:
            break  # 角度变化过大时终止

    # 第二部分：计算坐标轨迹
    lst_x, lst_y = [], []
    for i in np.arange(len(let_theta)):
        p = let_theta[i] * d / (2 * np.pi)
        x = p * np.cos(let_theta[i])
        y = p * np.sin(let_theta[i])
        lst_x.append(x)
        lst_y.append(y)

    # 第三部分：计算斜率
    lst_k = []
    for i in np.arange(len(let_theta) - 1):
        k = (lst_y[i] - lst_y[i + 1]) / (lst_x[i] - lst_x[i + 1])
        lst_k.append(k)

    # 第四部分：碰撞检测
    flag = 0
    k1 = lst_k[0]
    x1 = lst_x[0]
    y1 = lst_y[0]

    # 计算参考线参数
    k2 = (d2 / d1 + k1) / (1 + d2 * k1 / d1)  # 修正斜率计算公式
    b = d2 * np.sqrt(k1 ** 2 + 1) + y1 - k1 * x1  # 截距计算

    # 碰撞检测主循环
    for i in np.arange(len(lst_k)):
        if let_theta[i + 1] - theta > np.pi:
            ki = lst_k[i]
            xi = lst_x[i]
            yi = lst_y[i]

            # 计算距离（修正距离公式）
            numerator = np.abs(ki * (x1 - xi) + (y1 - yi))
            denominator = np.sqrt(ki ** 2 + 1)
            d_chair = numerator / denominator

            if d_chair < d2:
                flag = 1
                break

    return flag