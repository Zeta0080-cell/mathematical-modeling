import pandas as pd

supermarket = pd.read_csv('supclass.csv', encoding='utf-8')
supermarket.columns = ['一级品类', '二级品类', '三级品类', '四级品类']
print(supermarket)

