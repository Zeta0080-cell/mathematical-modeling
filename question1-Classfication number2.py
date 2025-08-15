import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows中文显示
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

#读入文件
supermarket = pd.read_csv('supclass.csv', encoding='utf-8')
supermarket.columns = ['一级品类', '二级品类', '三级品类', '四级品类']

#统计二级品类的数量
category_counts = supermarket['二级品类'].value_counts()  #value_counts()可以统计列中每个值出现的次数

# reindex()：确保所有目标品类都被包含（即使数据中没有也会显示为 0）。
target_categories = ['家居用品','保健品','烟酒水饮','粮油调味','冲调食品','冷藏乳制品','卫生用品','南北干货','家用清洁','休闲食品','个人清洁','冷冻类','冷藏类','婴童食品','服饰箱包']
category_counts = category_counts.reindex(target_categories, fill_value=0)
print(category_counts)

# 创建图表（调整尺寸适应长分类名）
plt.figure(figsize=(12, 6))

# 绘制水平条形图（更适合长文本标签）
ax = category_counts.sort_values().plot(
    kind='barh',  # 水平条形图
    color='#2b8cbe',
    edgecolor='black',
    width=0.8
)

# 图表装饰
plt.title('二级品类商品数量分布', fontsize=16, pad=20)
plt.xlabel('商品数量', fontsize=12)
plt.ylabel('二级品类', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)  # 横向网格线

# 在条形末端显示数值
for i, v in enumerate(category_counts.sort_values()):
    ax.text(v + 0.2, i, str(v),
           color='black',
           va='center',
           fontweight='bold')

# 自动调整布局
plt.tight_layout()
plt.show()