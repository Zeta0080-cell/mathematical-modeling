import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import fsolve


class BenchDragonModel:
    def __init__(self):
        # 板凳龙参数
        self.leader_length = 341  # 龙头长度(cm)
        self.body_length = 220  # 龙身长度(cm)
        self.tail_length = 220  # 龙尾长度(cm)
        self.bench_width = 30  # 板凳宽度(cm)
        self.num_benches = 223  # 板凳总数
        self.hole_diameter = 5.5  # 孔径(cm)
        self.hole_distance = 27.5  # 孔中心到板头距离(cm)

        # 运动参数
        self.v = 100  # 龙头前把手速度(cm/s)，可根据实际情况调整

        # 阿基米德螺线参数
        self.p = 2 * self.body_length  # 螺距，假设为两倍板凳长度
        self.b = self.p / (2 * np.pi)  # 螺线系数

    def archimedean_spiral(self, theta):
        """阿基米德螺线极坐标方程"""
        r = self.b * theta
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return r, x, y

    def dtheta_dt(self, theta, t):
        """微分方程：dθ/dt = v/(b*sqrt(θ²+1))"""
        return self.v / (self.b * np.sqrt(theta ** 2 + 1))

    def calculate_theta(self, t):
        """计算给定时间t时的极角θ"""
        # 初始条件：t=0时θ=0
        theta0 = 0
        # 时间点数组
        t_points = np.linspace(0, t, 100)
        # 解微分方程
        theta = odeint(self.dtheta_dt, theta0, t_points)
        return theta[-1][0]

    def calculate_leader_position(self, t):
        """计算龙头前把手在时间t时的位置"""
        theta = self.calculate_theta(t)
        r, x, y = self.archimedean_spiral(theta)
        return theta, x, y

    def calculate_next_bench(self, x1, y1, theta1, bench_length):
        """计算下一节板凳后把手的位置"""

        # 定义方程组
        def equations(vars):
            theta2, rho2 = vars
            eq1 = rho2 - (rho1 + (self.b) * (theta2 - theta1))
            eq2 = rho1 ** 2 + rho2 ** 2 - 2 * rho1 * rho2 * np.cos(theta2 - theta1) - bench_length ** 2
            return [eq1, eq2]

        # 初始猜测
        rho1 = np.sqrt(x1 ** 2 + y1 ** 2)
        theta2_guess = theta1 + 0.1
        rho2_guess = rho1 + (self.b) * (theta2_guess - theta1)

        # 解方程组
        theta2, rho2 = fsolve(equations, (theta2_guess, rho2_guess))
        x2 = rho2 * np.cos(theta2)
        y2 = rho2 * np.sin(theta2)

        return theta2, x2, y2

    def calculate_velocity(self, x1, y1, x2, y2, v1):
        """计算后把手的速度"""
        # 计算切线斜率k1和k2
        theta1 = np.arctan2(y1, x1)
        k1 = (np.sin(theta1) + theta1 * np.cos(theta1)) / (np.cos(theta1) - theta1 * np.sin(theta1))

        theta2 = np.arctan2(y2, x2)
        k2 = (np.sin(theta2) + theta2 * np.cos(theta2)) / (np.cos(theta2) - theta2 * np.sin(theta2))

        # AB直线的斜率
        if x1 != x2:
            k = (y1 - y2) / (x1 - x2)
        else:
            k = np.inf

        # 计算角度α和β
        if k != np.inf and k1 != np.inf:
            alpha = np.arctan(np.abs((k1 - k) / (1 + k * k1)))
        else:
            alpha = np.pi / 2

        if k != np.inf and k2 != np.inf:
            beta = np.arctan(np.abs((k2 - k) / (1 + k * k2)))
        else:
            beta = np.pi / 2

        # 速度迭代公式
        if np.cos(beta) != 0:
            v2 = v1 * np.cos(alpha) / np.cos(beta)
        else:
            v2 = v1  # 避免除以零

        return v2

    def simulate_dragon(self, total_time, time_step):
        """模拟板凳龙的运动"""
        # 初始化存储数组
        times = np.arange(0, total_time + time_step, time_step)
        num_points = len(times)

        # 存储所有板凳的位置 (x, y) 和速度
        positions = np.zeros((self.num_benches, num_points, 2))
        velocities = np.zeros((self.num_benches, num_points))

        for i, t in enumerate(times):
            # 计算龙头前把手位置
            theta1, x1, y1 = self.calculate_leader_position(t)
            positions[0, i, :] = [x1, y1]
            velocities[0, i] = self.v

            # 递推计算后续板凳位置
            for bench_idx in range(1, self.num_benches):
                # 确定当前板凳长度
                if bench_idx == 0:
                    bench_len = self.leader_length
                elif bench_idx == self.num_benches - 1:
                    bench_len = self.tail_length
                else:
                    bench_len = self.body_length

                # 获取前一个板凳的位置
                prev_x, prev_y = positions[bench_idx - 1, i, :]
                prev_theta = np.arctan2(prev_y, prev_x)

                # 计算当前板凳后把手位置
                theta2, x2, y2 = self.calculate_next_bench(prev_x, prev_y, prev_theta, bench_len)
                positions[bench_idx, i, :] = [x2, y2]

                # 计算当前板凳速度
                if bench_idx > 0:
                    prev_v = velocities[bench_idx - 1, i]
                    v = self.calculate_velocity(prev_x, prev_y, x2, y2, prev_v)
                    velocities[bench_idx, i] = v

        return times, positions, velocities

    def plot_dragon(self, positions, frame):
        """绘制板凳龙在某一时刻的形状"""
        plt.figure(figsize=(10, 10))

        # 绘制阿基米德螺线
        theta = np.linspace(0, 4 * np.pi, 1000)
        r = self.b * theta
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        plt.plot(x, y, 'b-', alpha=0.3, label='Archimedean Spiral')

        # 绘制板凳龙
        x_pos = positions[:, frame, 0]
        y_pos = positions[:, frame, 1]
        plt.plot(x_pos, y_pos, 'ro-', markersize=3, linewidth=1, label='Bench Dragon')

        # 标记龙头
        plt.plot(x_pos[0], y_pos[0], 'go', markersize=8, label='Dragon Head')

        plt.title(f'Bench Dragon Simulation at Time = {frame * 0.1:.1f}s')
        plt.xlabel('X Position (cm)')
        plt.ylabel('Y Position (cm)')
        plt.axis('equal')
        plt.legend()
        plt.grid(True)
        plt.show()


# 示例使用
if __name__ == "__main__":
    model = BenchDragonModel()

    # 模拟10秒的运动，时间步长0.1秒
    total_time = 10
    time_step = 0.1
    times, positions, velocities = model.simulate_dragon(total_time, time_step)

    # 绘制第50帧(5秒时)的板凳龙形状
    model.plot_dragon(positions, 50)

    # 输出部分结果
    print("龙头位置示例(前5秒):")
    for i in range(0, 50, 10):
        print(f"Time {times[i]:.1f}s: ({positions[0, i, 0]:.1f}, {positions[0, i, 1]:.1f})")

    print("\n龙尾速度示例(前5秒):")
    for i in range(0, 50, 10):
        print(f"Time {times[i]:.1f}s: {velocities[-1, i]:.1f} cm/s")