import numpy as np
from crashjudge import judge  # 用于判断是否发生碰撞

v0 = 1  # 无关速度
D = 9  # 调头空间的直径

for d in np.arange(0.55, 0.4, -0.01):
    theta_min = D * np.pi / d  # 确定进入调头空间时的极角theta
    for theta in np.arange(theta_min + 6, theta_min, -0.1):
        flag = judge(theta, d, v0)
        if flag:
            break
    if flag:
        break

# 判断当前模型是否在调头空间外有极化碰撞
for d in np.arange(d + 0.01, d - 0.01, -0.0001):
    theta_min = D * np.pi / d
    for theta in np.arange(theta_min + 6, theta_min, -0.1):
        flag = judge(theta, d, v0)
        if flag:
            break
    if flag:
        break

for d in np.arange(d + 0.0001, d - 0.0001, -0.00001):
    theta_min = D * np.pi / d
    for theta in np.arange(theta_min + 6, theta_min, -0.1):
        flag = judge(theta, d, v0)
        if flag:
            break
    if flag:
        break

for d in np.arange(d + 0.00001, d - 0.00001, -0.000001):
    theta_min = D * np.pi / d
    for theta in np.arange(theta_min + 6, theta_min, -0.1):
        flag = judge(theta, d, v0)
        if flag:
            break
    if flag:
        break

for d in np.arange(d + 0.000001, d - 0.000001, -0.0000001):
    theta_min = D * np.pi / d
    for theta in np.arange(theta_min + 6, theta_min, -0.1):
        flag = judge(theta, d, v0)
        if flag:
            break
    if flag:
        break

# 细化最小的媒距
print(d)  # 输出在调头空间外不会发生碰撞的最小的媒距