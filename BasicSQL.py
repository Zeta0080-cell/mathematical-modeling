import pandas as pd
import dask.dataframe as dd
# 读取数据（假设您的数据包含'sdate'列）
ddf = dd.read_csv('BOSS.csv',encoding='utf-8')

chunk_size = 1000000  # 每个文件保存100万行
for i, chunk in enumerate(pd.read_csv('BOSS.csv', chunksize=chunk_size)):
    chunk.to_excel(f'BOSS{i+1}.xlsx', index=False)

print('completed')
