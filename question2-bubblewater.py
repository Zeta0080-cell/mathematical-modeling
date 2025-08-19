import pandas as pd

df = pd.read_csv('BOSS.csv',encoding='utf-8')

#筛选碳酸饮料的数据
bubble=df[df['mysl_category_name_lv3']=='碳酸饮料']

bubble.to_csv('bubblewater.csv', index=False, encoding='utf-8')

print("complete")