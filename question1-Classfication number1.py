import pandas as pd
import matplotlib.pyplot as plt

supermarket = pd.read_csv('supclass.csv', encoding='utf-8')

supermarket.columns = ['一级品类', '二级品类', '三级品类', '四级品类']

# 统计一级品类的数量
category_counts = supermarket['一级品类'].value_counts()  #value_counts()可以统计列中每个值出现的次数

# reindex()：确保所有目标品类都被包含（即使数据中没有也会显示为 0）。
target_categories = ['非食', '医疗保健', '食品', '生鲜']
category_counts = category_counts.reindex(target_categories, fill_value=0)

print(category_counts)

# 3. 可视化
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
category_counts.plot(kind='bar', color='skyblue')
plt.title('一级品类数量统计')
plt.xlabel('品类')
plt.ylabel('数量')
plt.xticks(rotation=45)
plt.show()