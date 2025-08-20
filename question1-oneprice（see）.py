import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体和样式
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
mpl.rcParams['axes.unicode_minus'] = False

# 数据准备
categories = ['医疗保健', '生鲜', '非食', '食品']
sales = [244070.6, 794331.52, 5595646.92, 13306258.27]
percentages = [1.22, 3.98, 28.06, 66.73]
colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2']

# --------------------- 图1：条形图 ---------------------
plt.figure(figsize=(8, 6))
bars = plt.bar(categories, sales, color=colors)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}',
             ha='center', va='bottom', fontsize=10)

plt.title('一级品类销售额对比', fontsize=14, pad=20)
plt.ylabel('销售额（元）', fontsize=12)
plt.xticks(rotation=0)  # 水平显示标签

# 显示第一个图表
plt.show()

# --------------------- 图2：饼状图 ---------------------
plt.figure(figsize=(8, 6))
explode = (0, 0, 0.1, 0.1)  # 突出显示两个主要品类
wedges, texts, autotexts = plt.pie(percentages,
                                  explode=explode,
                                  colors=colors,
                                  autopct='%1.1f%%',
                                  startangle=90,
                                  pctdistance=0.8,
                                  textprops={'fontsize':12})

# 添加旁注（图例）
plt.legend(wedges, categories,
          title="品类分类",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

# 美化百分比标签
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

plt.title('销售额占比分布', fontsize=14, pad=20)
plt.axis('equal')  # 保证是正圆形

# 显示第二个图表
plt.tight_layout()
plt.show()