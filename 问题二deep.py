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
        self.v = 100  # 龙头前把手速度(cm/s)

        # 阿基米德螺线参数（螺距p=55cm）
        self.p = 55  # 螺距(cm)
        self.b = self.p / (2 * np.pi)  # 螺线系数

    def archimedean_spiral(self, theta):
        """阿基米德螺线极坐标方程 r = b*theta"""
        r = self.b * theta
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return r, x, y

    def dtheta_dt(self, theta, t):
        """微分方程：dθ/dt = v/(b*sqrt(θ²+1))"""
        return self.v / (self.b * np.sqrt(theta ** 2 + 1))

    def calculate_theta(self, t):
        """计算给定时间t时的极角θ"""
        theta0 = 0  # 初始条件：t=0时θ=0
        t_points = np.linspace(0, t, 100)
        theta = odeint(self.dtheta_dt, theta0, t_points)
        return theta[-1][0]

    def calculate_leader_position(self, t):
        """计算龙头前把手在时间t时的位置"""
        theta = self.calculate_theta(t)
        return self.archimedean_spiral(theta)

    def calculate_next_bench(self, x1, y1, theta1, bench_length):
        """计算下一节板凳后把手的位置"""

        def equations(vars):
            theta2, rho2 = vars
            rho1 = np.sqrt(x1 ** 2 + y1 ** 2)
            eq1 = rho2 - (rho1 + self.b * (theta2 - theta1))
            eq2 = rho1 ** 2 + rho2 ** 2 - 2 * rho1 * rho2 * np.cos(theta2 - theta1) - bench_length ** 2
            return [eq1, eq2]

        rho1 = np.sqrt(x1 ** 2 + y1 ** 2)
        theta2, rho2 = fsolve(equations, (theta1 + 0.1, rho1 + 0.1))
        return theta2, rho2 * np.cos(theta2), rho2 * np.sin(theta2)

    def simulate_dragon(self, total_time, time_step):
        """模拟板凳龙的运动"""
        times = np.arange(0, total_time + time_step, time_step)
        positions = np.zeros((self.num_benches, len(times), 2))

        for i, t in enumerate(times):
            # 计算龙头位置
            _, x1, y1 = self.calculate_leader_position(t)
            positions[0, i] = [x1, y1]

            # 计算后续板凳位置
            for bench_idx in range(1, self.num_benches):
                prev_x, prev_y = positions[bench_idx - 1, i]
                prev_theta = np.arctan2(prev_y, prev_x)

                # 确定板凳长度
                if bench_idx == self.num_benches - 1:
                    bench_len = self.tail_length
                elif bench_idx == 0:
                    bench_len = self.leader_length
                else:
                    bench_len = self.body_length

                _, x2, y2 = self.calculate_next_bench(prev_x, prev_y, prev_theta, bench_len)
                positions[bench_idx, i] = [x2, y2]

        return times, positions


class BenchDragonCollision(BenchDragonModel):
    def __init__(self):
        super().__init__()
        # 碰撞检测参数
        self.d1 = self.hole_distance  # 把手中心到板头距离
        self.d2 = self.bench_width / 2  # 半板宽
        self.gamma = np.arctan(self.d2 / self.d1)  # 夹角γ

    def line_intersection(self, k1, b1, k2, b2):
        """计算两条直线的交点"""
        if k1 == np.inf and k2 == np.inf:
            return (np.nan, np.nan)
        elif k1 == np.inf:
            return (b1, k2 * b1 + b2)
        elif k2 == np.inf:
            return (b2, k1 * b2 + b1)
        elif abs(k1 - k2) < 1e-6:
            return (np.nan, np.nan)
        else:
            x = (b2 - b1) / (k1 - k2)
            return (x, k1 * x + b1)

    def calculate_corner_points(self, x1, y1, x2, y2):
        """计算板凳的四个角点坐标"""
        if x1 == x2:
            k = np.inf
            b = x1
        else:
            k = (y2 - y1) / (x2 - x1)
            b = y1 - k * x1

        # 计算旋转后的直线
        def rotated_line(k, angle):
            if k == np.inf:
                return (1 / np.tan(angle), x1)
            tan_a = np.tan(angle)
            new_k = (tan_a + k) / (1 - k * tan_a)
            return (new_k, y1 - new_k * x1)

        # 计算平移后的直线
        def translated_line(k, b, distance):
            if k == np.inf:
                return (k, b + distance)
            angle = np.arctan(k)
            dx = distance * np.cos(angle)
            dy = distance * np.sin(angle)
            return (k, b - dy + k * dx)

        # 计算四条边线
        k2, b2 = rotated_line(k, self.gamma)  # a2
        k4, b4 = rotated_line(k, -self.gamma)  # a4
        k3, b3 = translated_line(k, b, self.d2)  # a3
        k3_opp, b3_opp = translated_line(k, b, -self.d2)  # 另一侧a3

        # 计算四个角点
        A1 = self.line_intersection(k2, b2, k3, b3)
        A2 = self.line_intersection(k4, b4, k3, b3)
        A3 = self.line_intersection(k2, b2, k3_opp, b3_opp)
        A4 = self.line_intersection(k4, b4, k3_opp, b3_opp)

        return [A1, A2, A3, A4]

    def point_to_line_distance(self, point, line_p1, line_p2):
        """计算点到直线的距离"""
        x0, y0 = point
        x1, y1 = line_p1
        x2, y2 = line_p2

        if x1 == x2 and y1 == y2:
            return np.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return numerator / denominator

    def check_collision(self, positions, frame_idx):
        """检测指定帧的碰撞情况"""
        collision = False
        min_distance = np.inf

        # 收集所有角点和边线
        all_corners = []
        bench_lines = []

        for i in range(self.num_benches - 1):
            x1, y1 = positions[i, frame_idx]
            x2, y2 = positions[i + 1, frame_idx]

            corners = self.calculate_corner_points(x1, y1, x2, y2)
            all_corners.extend(corners)
            bench_lines.append(((x1, y1), (x2, y2)))

        # 检查每个角点到所有边线的距离
        for corner in all_corners:
            if np.isnan(corner[0]):
                continue

            for line in bench_lines:
                dist = self.point_to_line_distance(corner, line[0], line[1])
                if dist < min_distance:
                    min_distance = dist
                if dist < self.d2:
                    collision = True

        return collision, min_distance

    def simulate_with_collision(self, total_time, time_step):
        """带碰撞检测的完整模拟"""
        times, positions = self.simulate_dragon(total_time, time_step)
        collision_flags = []
        min_distances = []

        for i in range(len(times)):
            collision, min_dist = self.check_collision(positions, i)
            collision_flags.append(collision)
            min_distances.append(min_dist)

        return times, positions, collision_flags, min_distances

    def plot_dragon(self, positions, frame_idx):
        """绘制指定帧的板凳龙状态"""
        plt.figure(figsize=(10, 10))

        # 绘制阿基米德螺线
        theta = np.linspace(0, 4 * np.pi, 1000)
        r = self.b * theta
        plt.plot(r * np.cos(theta), r * np.sin(theta), 'b-', alpha=0.3, label='Spiral')

        # 绘制板凳中心线
        x = positions[:, frame_idx, 0]
        y = positions[:, frame_idx, 1]
        plt.plot(x, y, 'ro-', markersize=3, label='Centers')

        # 绘制每个板凳的轮廓和角点
        for i in range(self.num_benches - 1):
            x1, y1 = positions[i, frame_idx]
            x2, y2 = positions[i + 1, frame_idx]

            corners = self.calculate_corner_points(x1, y1, x2, y2)
            corners = np.array([c for c in corners if not np.isnan(c[0])])

            if len(corners) >= 2:
                # 绘制轮廓
                plt.plot([corners[0, 0], corners[1, 0]], [corners[0, 1], corners[1, 1]], 'g-')
                plt.plot([corners[2, 0], corners[3, 0]], [corners[2, 1], corners[3, 1]], 'g-')
                plt.plot([corners[0, 0], corners[2, 0]], [corners[0, 1], corners[2, 1]], 'g-')
                plt.plot([corners[1, 0], corners[3, 0]], [corners[1, 1], corners[3, 1]], 'g-')
                # 绘制角点
                plt.plot(corners[:, 0], corners[:, 1], 'gs', markersize=4)

        plt.title(f'Bench Dragon at t={frame_idx * time_step:.1f}s (p={self.p}cm)')
        plt.xlabel('X (cm)')
        plt.ylabel('Y (cm)')
        plt.axis('equal')
        plt.legend()
        plt.grid(True)
        plt.show()


# 示例使用
if __name__ == "__main__":
    model = BenchDragonCollision()

    # 模拟10秒，步长0.1秒
    total_time = 10.0
    time_step = 0.1
    times, positions, collisions, min_dists = model.simulate_with_collision(total_time, time_step)

    # 绘制第50帧(5秒)
    model.plot_dragon(positions, 50)

    # 打印碰撞检测结果
    print("碰撞检测结果(前5秒):")
    for i in range(0, 50, 10):
        status = "碰撞" if collisions[i] else "安全"
        print(f"时间 {times[i]:.1f}s: {status}, 最小距离: {min_dists[i]:.2f}cm")

    # 检查是否有碰撞发生
    if any(collisions):
        first_collision = times[np.argmax(collisions)]
        print(f"\n首次碰撞发生在 {first_collision:.1f} 秒")
    else:
        print("\n模拟期间未检测到碰撞")