import matplotlib.pyplot as plt

# 数据准备
categories = ['医疗保健', '生鲜', '非食', '食品']
sales = [11360, 102709, 3263451, 2012319]

# 设置中文字体（Windows系统可用'SimHei'，Mac系统可用'Arial Unicode MS'）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))

# 使用更商务的蓝灰色系配色
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# 绘制柱状图
bars = ax.bar(categories, sales, color=colors, width=0.6,
              edgecolor='white', linewidth=1, alpha=0.9)

# 添加数据标签（自动千分位格式化）
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.,
            height * 1.02,
            f'{height:,}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold')

# 美化图表
ax.set_title('一级品类销售数量对比', fontsize=14, pad=20, fontweight='bold')
ax.set_ylabel('销售数量', fontsize=12, labelpad=10)

# 移除网格线（去除虚线）
ax.grid(False)

# 调整坐标轴样式
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.5)
ax.spines['bottom'].set_linewidth(0.5)

# 优化刻度标签
ax.tick_params(axis='both', which='both', length=0)  # 隐藏刻度线
plt.xticks(fontsize=11)
plt.yticks(fontsize=10)

# 添加浅色背景
ax.set_facecolor('#f9f9f9')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.savefig('category_sales.png', dpi=300, bbox_inches='tight')
plt.show()