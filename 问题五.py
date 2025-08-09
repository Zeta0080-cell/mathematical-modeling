import numpy as np
from velocitytheta import v_theta  # 用于计算速度和位置

# 参数初始化
v0 = 1  # 光头初始速度
v_max = 2  # 最大允许速度
theta0 = 16.6319611  # 光头0时刻时的极角
theta_chair0_3 = 14.1235657  # 第一节光身前把手到达盘出蝶镜时光头的位置参数theta

# 初始化存储列表
let_theta0 = np.arange(theta0 - np.pi, theta_chair0_3, 0.001)
let_v = []
let_flag = []
let_theta = []

# 第一阶段：粗略计算速度变化
for theta0 in let_theta0:
    [theta, v, flag] = v_theta(theta0, 4, 0, v0)
    let_theta.append(theta)
    let_v.append(v)
    let_flag.append(flag)

# 进行两次迭代计算
for j in range(2):
    for i in range(len(let_theta0)):
        theta_last = let_theta[i]
        v_last = let_v[i]
        flag_last = let_flag[i]
        [theta, v, flag] = v_theta(theta_last, flag_last, i, v_last)
        let_theta[i] = theta
        let_v[i] = v
        let_flag[i] = flag

# 找到速度最大的位置
theta0_max = let_theta0[let_v.index(max(let_v))]  # 速度最大时光头的位置参数theta

# 第二阶段：在速度最大位置附近细分计算
let_theta0 = np.arange(theta0_max - 0.001, theta0_max + 0.001, 0.000001)
let_v = []
let_flag = []
let_theta = []

for theta0 in let_theta0:
    [theta, v, flag] = v_theta(theta0, 4, 0, v0)
    let_theta.append(theta)
    let_v.append(v)
    let_flag.append(flag)

# 再进行两次迭代计算
for j in range(2):
    for i in range(len(let_theta0)):
        theta_last = let_theta[i]
        v_last = let_v[i]
        flag_last = let_flag[i]
        [theta, v, flag] = v_theta(theta_last, flag_last, i, v_last)
        let_theta[i] = theta
        let_v[i] = v
        let_flag[i] = flag

# 计算并输出最大速度
vO_max = v_max * v0 / max(let_v)  # 计算光头的最大速度
print(f"原始最大速度: {max(let_v)}")
print(f"调整后的最大速度: {vO_max}")