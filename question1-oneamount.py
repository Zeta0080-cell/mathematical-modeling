import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('oneamount.csv', header=None, names=['销售数量', '一级品类'])

# 只需要前两列，去掉第三列
df = df[['销售数量', '一级品类']]

# 按商品品类分组并计算销售数量总和
result = df.groupby('一级品类')['销售数量'].sum().reset_index()

# 打印结果
print("各商品品类的销售数量统计:")
print(result)


# 设置中文字体（确保系统有支持的中文字体）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建图表
plt.figure(figsize=(10, 6))

# 绘制条形图
bars = plt.bar(result['一级品类'], result['销售数量'], color=['#4CAF50', '#2196F3', '#FFC107'])

# 添加标题和标签
plt.title('各商品品类销售数量', fontsize=15)
plt.xlabel('商品品类', fontsize=12)
plt.ylabel('销售数量', fontsize=12)

# 在每个条形上显示具体数值
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=12)

# 旋转x轴标签（如果品类名称较长）
plt.xticks(rotation=45)

# 自动调整布局
plt.tight_layout()

# 显示图表
plt.show()

# 创建饼图
plt.figure(figsize=(8, 8))

# 绘制饼图
patches, texts, autotexts = plt.pie(
    result['销售数量'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['#4CAF50', '#2196F3', '#FFC107'],
    textprops={'fontsize': 12}
)

# 设置标题
plt.title('各商品品类销售数量占比', fontsize=15)

# 确保饼图是正圆形
plt.axis('equal')

# 显示图表
plt.show()