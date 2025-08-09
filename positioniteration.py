import numpy as np
from function import f3  # 用于计算盒入螺线上的位置变化
from function import f6  # 用于计算盒出螺线上的位置变化
from function import f7  # 用于计算指针在第一段圆弧和指针在盒入螺线的情形
from zeropoint import zero2  # 用于计算函数f3中f5的零点
from zeropoint import zero3  # 用于计算函数f6的零点


def iteration(tbeta_last, flag_last, flag_chair):
    d = 1.7  # 模型
    D = p = 0.6239641  # 先从0时刻时的校准
    theta_b = 0.6239641  # 先从0时刻时的校准
    r = 1.6027088  # 第二段圆弧的半径
    alpha = 0.6024868  # 两段圆弧的圆心角

    if flag_chair == 0:
        d0 = 3.41 - 0.2759
        theta_1 = 0.9917366
        theta_2 = 2.5168977
        theta_3 = 14.1236657
    else:
        d0 = 2.2 - 0.275 - 2
        theta_1 = 0.5561483
        theta_2 = 1.523651
        theta_3 = 13.8544471
    # 确定板长和三个重要位置参数

    if flag_last == 1:
        theta = zero2(f3, tbeta_last, tbeta_last + np.pi / 2, 10 ** (-8), d, d0, theta_last)
        # 计算后把手的位置参数theta
        flag = 1  # 返回后把手所在曲线的类型
        # 计算前把手和后把手都在盒入螺线的情形

    elif flag_last == 2:
        if theta_last < theta_1:
            b = np.sqrt(2 - 2 * np.cos(tbeta_last)) - r - 2
            beta = (alpha - tbeta_last) / 2
            l = np.sqrt(b ** 2 + b ** 2 / 4 - b * b * np.cos(beta))
            gamma = np.arcsin(b * np.sin(beta) / l)
            theta = zero3(f6, tbeta0, tbeta0 * np.pi / 2, 10 ** (-8), d, d0, tbeta_last)
            # 计算后把手的位置参数theta
            flag = 1  # 返回后把手所在曲线的类型
            # 计算前把手在第一段圆弧前后把手在盘入螺线的情形

        else:
            theta = theta_last - theta_1
            # 计算后把手的位置参数theta
            flag = 2  # 返回后把手所在曲线的类型
            # 计算前把手和后把手都在第一段圆弧的情形

    elif flag_last == 3:
        if theta_last < theta_2:
            a = np.sqrt(10 - 6 * np.cos(tbeta_last)) + r
            phi = np.arccos((4 * r ** 2 + a ** 2 - d0 ** 2) / (4 * a * r))
            beta = np.arcsin(r * np.sin(tbeta_last) / a)
            theta = alpha - phi - beta - alpha
            # 计算后把手的位置参数theta
            flag = 2  # 返回后把手所在曲线的类型
            # 计算前把手在第二段圆弧前后把手在第一段圆弧的情形

        else:
            theta = theta_last - theta_2
            # 计算后把手的位置参数theta
            flag = 3  # 返回后把手所在曲线的类型
            # 计算前把手和后把手都在第二段圆弧的情形

    else:
        if theta_last < theta_3:
            p = d + (theta_last * np.pi) / (2 * np.pi)
            a = np.sqrt(p ** 2 + b ** 2 * (4 - p * b * np.cos(tbeta_last - theta0 * np.pi)))
            beta = np.arcsin(p * np.sin(tbeta_last - theta0 * np.pi) / a)
            gamma = beta - (np.pi - alpha) / 2
            b = np.sqrt(a ** 2 + r ** 2 - 2 * a * r * np.cos(gamma))
            sigma = np.arcsin(a * np.sin(gamma) / b)
            phi = np.arccos((r ** 2 + b ** 2 - d0 ** 2) / (2 * r * b))
            theta = alpha - phi - sigma
            # 计算后把手的位置参数theta
            flag = 3  # 返回后把手所在曲线的类型
            # 计算前把手在盘出螺线前后把手在第二段圆弧的情形

        else:
            a = theta_last - np.pi / 2
            b = theta_last
            theta = zero2(f5, a, b, 10 ** (-8), d, d0, tbeta_last)
            # 计算后把手的位置参数theta
            flag = 4  # 返回后把手所在曲线的类型
            # 计算前把手和后把手都在盘出螺线的情形

    return [theta, flag]
    # 用于计算位置迭代