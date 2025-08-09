import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

from 问题二deep import BenchDragonCollision


class BenchDragonOptimizer(BenchDragonCollision):
    def __init__(self):
        super().__init__()
        # 调头空间参数（根据题目要求设置）
        self.turn_area_radius = 500  # 调头空间半径(cm)
        self.turn_area_center = (0, 0)  # 调头空间中心

    def calculate_termination_time(self, pitch):
        """计算给定螺距下的盘入终止时间"""
        # 更新螺距参数
        self.p = pitch
        self.b = self.p / (2 * np.pi)

        # 模拟运动直到龙头进入调头空间
        total_time = 30.0  # 最大模拟时间
        time_step = 0.1
        times, positions = self.simulate_dragon(total_time, time_step)

        # 计算龙头到中心的距离
        distances = np.sqrt(positions[0, :, 0] ** 2 + positions[0, :, 1] ** 2)

        # 找到首次进入调头空间的时刻
        inside_indices = np.where(distances <= self.turn_area_radius)[0]
        if len(inside_indices) > 0:
            return times[inside_indices[0]]
        else:
            return total_time  # 未能在模拟时间内进入

    def is_inside_turn_area(self, pitch):
        """检查给定螺距下龙头最终位置是否在调头空间内"""
        termination_time = self.calculate_termination_time(pitch)
        _, x, y = self.calculate_leader_position(termination_time)
        distance = np.sqrt(x ** 2 + y ** 2)
        return distance <= self.turn_area_radius

    def find_boundary_pitch(self, pitch_min=30, pitch_max=100):
        """二分查找法寻找恰好到达边界的螺距"""
        low = pitch_min
        high = pitch_max
        tolerance = 0.1  # 精度(cm)

        while high - low > tolerance:
            mid = (low + high) / 2
            if self.is_inside_turn_area(mid):
                high = mid
            else:
                low = mid

        return (low + high) / 2

    def optimize_pitch(self):
        """优化螺距使龙头恰好到达调头空间边界"""
        # 先找到大致范围
        test_pitches = np.linspace(30, 100, 10)
        inside_flags = [self.is_inside_turn_area(p) for p in test_pitches]

        # 找到从外部到内部的转折点
        for i in range(1, len(test_pitches)):
            if inside_flags[i - 1] == False and inside_flags[i] == True:
                boundary_pitch = self.find_boundary_pitch(test_pitches[i - 1], test_pitches[i])
                return boundary_pitch

        # 如果没有找到转折点，扩大搜索范围
        return self.find_boundary_pitch(10, 200)

    def plot_termination_position(self, pitch):
        """绘制给定螺距下的终止位置"""
        termination_time = self.calculate_termination_time(pitch)
        times, positions = self.simulate_dragon(termination_time, 0.1)

        plt.figure(figsize=(10, 10))

        # 绘制阿基米德螺线
        theta = np.linspace(0, 4 * np.pi, 1000)
        r = self.b * theta
        plt.plot(r * np.cos(theta), r * np.sin(theta), 'b-', alpha=0.3, label='Spiral')

        # 绘制板凳龙中心线
        x = positions[:, -1, 0]
        y = positions[:, -1, 1]
        plt.plot(x, y, 'ro-', markersize=3, label='Centers')

        # 绘制调头空间
        circle = plt.Circle(self.turn_area_center, self.turn_area_radius,
                            color='g', fill=False, linestyle='--', label='Turn Area')
        plt.gca().add_patch(circle)

        # 标记龙头位置
        plt.plot(x[0], y[0], 'go', markersize=8, label='Head Position')

        plt.title(f'Termination Position (p={pitch:.1f}cm, t={termination_time:.1f}s)')
        plt.xlabel('X (cm)')
        plt.ylabel('Y (cm)')
        plt.axis('equal')
        plt.legend()
        plt.grid(True)
        plt.show()


# 示例使用
if __name__ == "__main__":
    optimizer = BenchDragonOptimizer()

    # 示例1：螺距太大（龙头在调头空间外）
    large_pitch = 80
    print(f"螺距={large_pitch}cm时：")
    termination_time = optimizer.calculate_termination_time(large_pitch)
    _, x, y = optimizer.calculate_leader_position(termination_time)
    distance = np.sqrt(x ** 2 + y ** 2)
    print(f"终止时间: {termination_time:.1f}s")
    print(f"龙头位置: ({x:.1f}, {y:.1f}), 距离中心: {distance:.1f}cm")
    print("是否在调头空间内:", "是" if distance <= optimizer.turn_area_radius else "否")
    optimizer.plot_termination_position(large_pitch)

    # 示例2：螺距太小（龙头在调头空间内）
    small_pitch = 40
    print(f"\n螺距={small_pitch}cm时：")
    termination_time = optimizer.calculate_termination_time(small_pitch)
    _, x, y = optimizer.calculate_leader_position(termination_time)
    distance = np.sqrt(x ** 2 + y ** 2)
    print(f"终止时间: {termination_time:.1f}s")
    print(f"龙头位置: ({x:.1f}, {y:.1f}), 距离中心: {distance:.1f}cm")
    print("是否在调头空间内:", "是" if distance <= optimizer.turn_area_radius else "否")
    optimizer.plot_termination_position(small_pitch)

    # 寻找最佳螺距
    print("\n正在计算最佳螺距...")
    optimal_pitch = optimizer.optimize_pitch()
    termination_time = optimizer.calculate_termination_time(optimal_pitch)
    _, x, y = optimizer.calculate_leader_position(termination_time)
    distance = np.sqrt(x ** 2 + y ** 2)

    print(f"\n最佳螺距: {optimal_pitch:.2f}cm")
    print(f"终止时间: {termination_time:.1f}s")
    print(f"龙头位置: ({x:.1f}, {y:.1f}), 距离中心: {distance:.1f}cm")
    print("是否在调头空间边界:", abs(distance - optimizer.turn_area_radius) < 0.1)
    optimizer.plot_termination_position(optimal_pitch)