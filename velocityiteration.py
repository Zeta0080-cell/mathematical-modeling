import numpy as np
from function import f4  # 用于计算螺旋上速度的斜率


def iteration2(v_last, flag_last, flag, tbeta_last, tbeta, x_last, y_last, x, y):
    x1 = -0.7600091
    y1 = -1.5057264
    # 计算第一段圆弧的圆心坐标
    x2 = 1.7358935
    y2 = 2.4484020
    # 计算第二段圆弧的圆心坐标

    k_chair = (y_last - y) / (x_last - x)  # 计算板块的斜率
    v = -1

    if flag_last == 1 and flag == 1:
        k_v_last = f4(tbeta_last)
        k_v = f4(tbeta)
        # 计算前把手和后把手都在盘入螺线时两个速度的斜率

    elif flag_last == 2 and flag == 1:
        k_v_last = (x_last - x1) / (y_last - y1)
        k_v = f4(tbeta)
        # 计算前把手在第一段圆弧而后把手在盘入螺线时两个速度的斜率

    elif flag_last == 2 and flag == 2:
        v = v_last
        # 计算前把手和后把手都在第一段圆弧的情形

    elif flag_last == 3 and flag == 2:
        k_v_last = (x_last - x2) / (y_last - y2)
        k_v = (x - x1) / (y - y1)
        # 计算前把手在第二段圆弧而后把手在第一段圆弧时两个速度的斜率

    elif flag_last == 3 and flag == 3:
        v = v_last
        # 计算前把手和后把手都在第二段圆弧的情形

    elif flag_last == 4 and flag == 3:
        tbeta_last = tbeta_last + np.pi
        k_v_last = f4(tbeta_last)
        k_v = (x - x2) / (y - y2)
        # 计算前把手在盘出螺线前后把手在第二段圆弧时两个速度的斜率

    else:
        tbeta_last = tbeta_last + np.pi
        tbeta = tbeta + np.pi
        k_v_last = f4(tbeta_last)
        k_v = f4(tbeta)
        # 计算前把手和后把手都在盘出螺线时两个速度的斜率

    if v == -1:
        alpha1 = np.arctan(np.abs((k_v_last - k_chair) / (1 + k_v_last * k_chair)))
        alpha2 = np.arctan(np.abs((k_v - k_chair) / (1 + k_v * k_chair)))
        # 计算前把手和后把手的角度
        v = v_last * np.cos(alpha1) / np.cos(alpha2)  # 计算当前把手的速度

    return v
    # 用于计算速度迭代