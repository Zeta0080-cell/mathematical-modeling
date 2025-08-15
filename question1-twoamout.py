import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('twoamount.csv', header=None, names=['销售数量', '二级品类'])

df = df[['销售数量', '二级品类']]

# 按商品品类分组并计算销售数量总和
result = df.groupby('二级品类')['销售数量'].sum().reset_index()

# 打印结果
print("各商品品类的销售数量统计:")
print(result)

# 设置中文字体（确保系统有支持的中文字体）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建图表（横向条形图更适合品类名称显示）
plt.figure(figsize=(10, 6))

# 按销售数量排序
result_sorted = result.sort_values('销售数量', ascending=True)

# 绘制横向条形图
bars = plt.barh(result_sorted['二级品类'], result_sorted['销售数量'],
                color=plt.cm.tab20c.colors)

# 添加标题和标签
plt.title('各商品品类销售数量统计', fontsize=15, pad=20)
plt.xlabel('销售数量', fontsize=12)
plt.ylabel('商品品类', fontsize=12)

# 在每个条形末端显示具体数值
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
             f'{int(width)}',
             va='center', fontsize=10)

# 调整左边距确保品类名称显示完整
plt.subplots_adjust(left=0.3)

# 显示网格线（浅灰色，虚线）
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.show()

# 创建饼图
plt.figure(figsize=(10, 8))

# 过滤掉销售数量太小的品类（可选）
filtered = result[result['销售数量'] > result['销售数量'].sum()*0.05]

# 绘制饼图
wedges, texts, autotexts = plt.pie(
    filtered['销售数量'],
    labels=filtered['二级品类'],
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.tab20.colors,
    pctdistance=0.85,
    textprops={'fontsize': 10}
)

# 设置标题
plt.title('各商品品类销售数量占比', fontsize=15, pad=20)

# 添加图例（放在右侧）
plt.legend(wedges, filtered['二级品类'],
          title="商品品类",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

# 确保饼图是正圆形
plt.axis('equal')

plt.tight_layout()
plt.show()