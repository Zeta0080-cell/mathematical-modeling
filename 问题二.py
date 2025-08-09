import numpy as np
import pandas as pd
from function import f1  # 用于计算龙头位置随时间的变化
from function import f3  # 用于计算注入流量后的位置迭代
from function import f4  # 用于计算模具上速度的增长
from zeropoint import zero2  # 用于计算函数f3的零点
from number import round_decimal  # 用于保留6位小数
from cachingldge import judge  # 用于判断是否碰撞

# 参数初始化
d = 0.56  # 龙头直径
v0 = 1.0  # 初始速度
theta_init = 32 * np.pi / 180  # 初始角度（32度转弧度）

# 第一部分：精确碰撞检测
theta_collision = None
# 粗检测（步长0.01）
for theta in np.arange(theta_init, 0, -0.01):
    if judge(theta, d, v0):
        theta_collision = theta
        break

# 中等精度检测（步长0.0001）
if theta_collision is not None:
    for theta in np.arange(theta_collision + 0.01, theta_collision - 0.01, -0.0001):
        if judge(theta, d, v0):
            theta_collision = theta
            break

# 高精度检测（步长0.000001）
if theta_collision is not None:
    for theta in np.arange(theta_collision + 0.0001, theta_collision - 0.0001, -0.000001):
        if judge(theta, d, v0):
            theta_collision = theta
            break

# 计算碰撞时间（修正公式）
if theta_collision is not None:
    t_collision = (f1(theta_init) - f1(theta_collision)) / (4 * np.pi * v0)
    let_chain_theta = [theta_collision]
else:
    let_chain_theta = [theta_init]

# 第二部分：计算把手轨迹
for i in np.arange(223):
    if i == 0:
        d0 = 3.41 - 0.275 - 2  # 初始设计参数
    else:
        d0 = 2.2 - 0.275 - 2  # 后续设计参数

    theta_last = let_chain_theta[-1]
    theta = zero2(f3, theta_last, theta_last + np.pi / 2, 1e-8, d, d0, theta_last)
    let_chain_theta.append(theta)

    # 第三部分：计算坐标和速度场
    let_chair_xyv = []
    for i in np.arange(224):
        theta = let_chain_theta[i]
        x = d * theta * np.cos(theta) / (2 * np.pi)  # 修正坐标计算公式
        y = d * theta * np.sin(theta) / (2 * np.pi)
        let_chair_xyv.append([x, y, v0])  # 初始速度为v0

    let_chair_xyv = np.array(let_chair_xyv)

    # 第四部分：速度场迭代计算
    for i in np.arange(223):
        v_last = let_chair_xyv[i, 2]  # 上一个速度
        theta_last = let_chain_theta[i]
        theta = let_chain_theta[i + 1]

        # 获取坐标
        x_last, y_last = let_chair_xyv[i, 0], let_chair_xyv[i, 1]
        x, y = let_chair_xyv[i + 1, 0], let_chair_xyv[i + 1, 1]

        # 计算斜率
        k_chair = (y_last - y) / (x_last - x) if (x_last - x) != 0 else np.inf
        k_v_last = f4(theta_last)
        k_v = f4(theta)

        # 计算角度
        alpha1 = np.arctan(np.abs((k_v_last - k_chair) / (1 + k_v_last * k_chair)))
        alpha2 = np.arctan(np.abs((k_v - k_chair) / (1 + k_v * k_chair)))

        # 更新速度
        v = v_last * np.cos(alpha1) / np.cos(alpha2)
        let_chair_xyv[i + 1, 2] = v

    # 数据后处理
    let_chair_xyv = round_decimal(let_chair_xyv, 6)  # 保留6位小数
    df = pd.DataFrame(let_chair_xyv, columns=['x', 'y', 'velocity'])
    df.to_excel('result2.xlsx', index=False)