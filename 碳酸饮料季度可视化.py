import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 数据
months = ['2021-06', '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12',
          '2022-01', '2022-02', '2022-03', '2022-04', '2022-05']
seasonal_indices = [1.359, 2.298, 1.027, 1.033, 1.028, 0.448, 0.366, 1.336, 0.567, 0.690, 0.854, 0.854]

# 创建图表
plt.figure(figsize=(12, 6))

# 绘制折线图
plt.plot(months, seasonal_indices, marker='o', linewidth=2, markersize=6, markerfacecolor='red', markeredgecolor='darkred')

# 添加平均线（指数=1）
plt.axhline(y=1.0, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='平均水平 (指数=1)')

# 设置标题和标签
plt.title('碳酸饮料销售季节性指数变化趋势 (2021年6月-2022年5月)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('月份', fontsize=12)
plt.ylabel('季节性指数', fontsize=12)

# 设置纵轴范围，更好地显示波动
plt.ylim(0, 2.5)

# 旋转x轴标签以避免重叠
plt.xticks(rotation=45)

# 添加网格
plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

# 在每个数据点上添加数值标签
for i, v in enumerate(seasonal_indices):
    plt.annotate(f'{v:.3f}', (i, v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

# 添加图例
plt.legend()

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()