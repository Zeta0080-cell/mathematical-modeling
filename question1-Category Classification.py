import pandas as pd

# 最佳实践：自动读取表头 + 指定编码
supermarket = pd.read_csv('supclass.csv', encoding='utf-8')

# 如果想重命名列（可选）
supermarket.columns = ['一级品类', '二级品类', '三级品类', '四级品类']
print(supermarket)

