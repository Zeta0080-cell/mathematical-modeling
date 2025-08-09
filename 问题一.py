import numpy as np
import pandas as pd
from function import f2  # 用于计算龙头位置随时间的变化
from function import f3  # 用于计算盘入螺线上的位置迭代
from function import f4  # 用于计算螺线上速度的斜率
from zeropoint import zero1  # 用于计算函数f2的零点
from zeropoint import zero2  # 用于计算函数f3的零点
from number import round_decimal  # 用于保留6位小数（修正后的函数名）

# 参数初始化
d = 0.56  # 顺题
v0 = 1  # 初始速度
theta0 = 32 * np.pi / 180  # 初始角度转换为弧度（原32=np.pi有误）

# 第一部分：计算椅子角度轨迹
let_chair_theta = []
for t in np.arange(301):
    if t == 0:
        theta_chair0 = theta0
    else:
        theta_chair0 = zero1(f2, 0, theta0, 1e-8, theta0, v0, t, d)
    let_theta = [theta_chair0]

    for i in np.arange(223):
        d0 = 3.41 - 0.275 + 2 if i == 0 else 2.2 - 0.275 + 2  # 动态调整d0
        theta_last = let_theta[-1]
        theta = zero2(f3, theta_last, theta_last + np.pi / 2, 1e-8, d, d0, theta_last)
        let_theta.append(theta)

    let_chair_theta.append(let_theta)

let_chair_theta = np.array(let_chair_theta)

# 第二部分：计算椅子xy坐标
let_chair_xy = []
for t in np.arange(301):
    let_xy = []
    for i in np.arange(224):
        theta = let_chair_theta[t, i]
        x = d * theta * np.cos(theta) / (2 * np.pi)  # 修正原代码中的语法错误
        y = d * theta * np.sin(theta) / (2 * np.pi)
        let_xy.extend([x, y])
    let_chair_xy.append(let_xy)

let_chair_xy = np.array(let_chair_xy).T
let_chair_xy = round_decimal(let_chair_xy, 6)  # 保留6位小数

# 保存xy坐标结果
#df_xy = pd.DataFrame(let_chair_xy)
#df_xy.to_excel('result1_1.xlsx', index=False)

# 第三部分：计算速度场
let_chair_v = []
for t in np.arange(0, 301):
    let_v = [v0]
    for i in np.arange(223):
        # 获取前一个点和当前点的坐标
        x_last, y_last = let_chair_xy[2 * i, t], let_chair_xy[2 * i + 1, t]
        x, y = let_chair_xy[2 * (i + 1), t], let_chair_xy[2 * (i + 1) + 1, t]

        # 计算斜率
        k_chair = (y - y_last) / (x - x_last) if (x - x_last) != 0 else np.inf
        theta_last = let_chair_theta[t, i]
        theta = let_chair_theta[t, i + 1]
        k_y_last = f4(theta_last)
        k_y = f4(theta)

        # 计算角度差
        alpha1 = np.arctan(np.abs((k_y_last - k_chair) / (1 + k_y_last * k_chair)))
        alpha2 = np.arctan(np.abs((k_y - k_chair) / (1 + k_y * k_chair)))

        # 计算速度
        v = let_v[-1] * np.cos(alpha1) / np.cos(alpha2)
        let_v.append(v)

    let_chair_v.append(let_v)

let_chair_v = np.array(let_chair_v).T
let_chair_v = round_decimal(let_chair_v, 6)

# 保存速度结果
#df_v = pd.DataFrame(let_chair_v)
#df_v.to_excel('result1_2.xlsx', index=False)