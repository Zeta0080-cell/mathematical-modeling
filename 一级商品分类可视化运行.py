import pandas as pd
import matplotlib.pyplot as plt

# 1. 读取CSV文件（自动处理编码）
try:
    supermarket = pd.read_csv('supclass.csv', encoding='utf-8')
    print("✅ 文件读取成功！前5行数据预览：")
    print(supermarket.head())
except UnicodeDecodeError:
    # 如果utf-8失败，尝试其他编码
    supermarket = pd.read_csv('supclass.csv', encoding='gbk')
    print("⚠️  UTF-8解码失败，已自动切换GBK编码，前5行数据预览：")
    print(supermarket.head())

# 2. 重命名列（全中文）
supermarket.columns = ['一级品类', '二级品类', '三级品类', '四级品类']
print("\n📊 重命名后的列名：", supermarket.columns.tolist())

# 3. 统计一级品类数量
category_counts = supermarket['一级品类'].value_counts()
print("\n🔢 一级品类数量统计：")
print(category_counts)

# 4. 可视化（中文图表）
plt.figure(figsize=(10, 6))
category_counts.plot(
    kind='bar',
    color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
    edgecolor='black'
)

# 设置中文显示（需系统支持中文字体）
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

plt.title('一级品类商品数量分布', fontsize=16, pad=20)
plt.xlabel('商品大类', fontsize=12)
plt.ylabel('商品数量', fontsize=12)
plt.xticks(rotation=45, ha='right')  # x轴标签倾斜45度
plt.grid(axis='y', linestyle='--', alpha=0.7)  # 添加横向网格线

# 在柱子上方显示数值
for i, v in enumerate(category_counts):
    plt.text(i, v + 0.2, str(v), ha='center', va='bottom')

plt.tight_layout()  # 自动调整布局
plt.show()