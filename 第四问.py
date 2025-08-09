import numpy as np
import pandas as pd
from function import f2  # 用于计算龙头位置随时间的变化
from zeropoint import zerol  # 用于计算函数f2的零点
from number import number  # 用于保留6位小数
from positioniteration import iteration1  # 用于计算位置迭代
from velocityiteration import iteration2  # 用于计算速度迭代

# 参数初始化
d = 1.7  # 提示
v0 = 1  # 龙头速度
theta0 = 16.6319611  # 龙头0时刻时的视角
r = 1.5027088  # 第二段圆弧的半径
alpha = 3.0214868  # 两段圆弧的圆心角
t1 = 9.0808299  # 龙头到达第二段圆弧的时刻
t2 = 13.6212449  # 龙头到达盘山端线的时刻
x1 = -0.7606091
y1 = -1.3057264  # 第一段圆弧的圆心坐标
x2 = 1.7359325
y2 = 2.4484004  # 第二段圆弧的圆心坐标
theta1 = 16.0055376  # 第一段圆弧的进入点相对于圆心的锐角
theta2 = 0.8639449  # 第二段圆弧的离开点相对于圆心的锐角

# 初始化存储列表
let_chair_theta = []
let_chair_flag = []

# 计算龙头的位置参数theta和flag
for t in np.arange(-100, 101):
    if t < 0:
        theta_chain0 = zerol(f2, t, 100, 10 ** (-8), theta0, v0, t, d)
        flag_chain0 = 1
    elif t == 0:
        theta_chain0 = theta0
        flag_chain0 = 1
    elif t < t1:
        theta_chain0 = v0 * t + (2 - r)
        flag_chain0 = 2
    elif t < t2:
        theta_chain0 = v0 * t1 - (t - t1) / r
        flag_chain0 = 3
    else:
        theta_chain0 = zerol(f2, t, 100, 10 ** (-8), theta0, v0, -t + t2) - np.pi
        flag_chain0 = 4
    let_chair_theta.append(theta_chain0)
    let_chair_flag.append(flag_chain0)

# 计算把手的位置参数theta和flag
let_theta = [let_chair_theta[0]]
let_flag = [let_chair_flag[0]]
for i in np.arange(222):
    theta_last = let_theta[-1]  # 获得上一个把手的位置参数theta
    flag_last = let_flag[-1]  # 获得上一个把手所在曲线的类型参数flag
    theta, flag = iteration1(theta_last, flag_last, i)
    let_theta.append(theta)
    let_flag.append(flag)

let_chair_theta = np.array(let_theta)
let_chair_flag = np.array(let_flag)

# 计算把手的坐标(x,y)
let_chair_xy = []
for i in np.arange(201):
    lst = []
    for j in np.arange(224):
        flag = let_chair_flag[i, j] if let_chair_flag.ndim > 1 else let_chair_flag[j]
        theta = let_chair_theta[i, j] if let_chair_theta.ndim > 1 else let_chair_theta[j]

        if flag == 1:
            p = d + theta / (2 * np.pi)
            x = p * np.cos(theta)
            y = p * np.sin(theta)
        elif flag == 2:
            x = x1 + 2 * r * np.cos(theta1 + theta)
            y = y1 + 2 * r * np.sin(theta1 + theta)
        elif flag == 3:
            x = x2 + r * np.cos(theta2 + theta - alpha)
            y = y2 + r * np.sin(theta2 + theta - alpha)
        else:
            p = d + (theta + np.pi) / (2 * np.pi)
            x = p * np.cos(theta)
            y = p * np.sin(theta)
        lst.extend([x, y])
    let_chair_xy.append(lst)

let_chair_xy = np.array(let_chair_xy).T
let_chair_xy = number(let_chair_xy, 6)  # 保留6位小数
df = pd.DataFrame(let_chair_xy)
df.to_excel('result4_1.xlsx', index=False)  # 保存数据到Excel中

# 计算把手的速度
let_chair_v = []
for i in np.arange(201):
    let_v = [v0]
    for j in np.arange(223):
        flag_last = let_chair_flag[i, j] if let_chair_flag.ndim > 1 else let_chair_flag[j]
        theta_last = let_chair_theta[i, j] if let_chair_theta.ndim > 1 else let_chair_theta[j]
        flag = let_chair_flag[i, j + 1] if let_chair_flag.ndim > 1 else let_chair_flag[j + 1]
        theta = let_chair_theta[i, j + 1] if let_chair_theta.ndim > 1 else let_chair_theta[j + 1]
        x_last = let_chair_xy[2 * j, i] if let_chair_xy.shape[0] > 2 else let_chair_xy[0, j]
        y_last = let_chair_xy[2 * j + 1, i] if let_chair_xy.shape[0] > 2 else let_chair_xy[1, j]
        x = let_chair_xy[2 * (j + 1), i] if let_chair_xy.shape[0] > 2 else let_chair_xy[0, j + 1]
        y = let_chair_xy[2 * (j + 1) + 1, i] if let_chair_xy.shape[0] > 2 else let_chair_xy[1, j + 1]

        v_last = let_v[-1]  # 获得上一个把手的速度
        v = iteration2(v_last, flag_last, flag, theta_last, theta, x_last, y_last, x, y)
        let_v.append(v)
    let_chair_v.append(let_v)

let_chair_v = np.array(let_chair_v).T
let_chair_v = number(let_chair_v, 6)  # 保留6位小数
df = pd.DataFrame(let_chair_v)
df.to_excel('result4_2.xlsx', index=False)  # 保存数据到Excel中