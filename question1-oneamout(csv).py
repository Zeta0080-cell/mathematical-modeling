import pandas as pd

# 读取数据
df = pd.read_csv('suprevenue.csv')

# 选择需要的列（第3列和第4列）
selected_columns = df.iloc[:, [3, 4]]  # 所有行，第3和第4列

# 保存到新文件（例如命名为 'selected_data.csv'）
selected_columns.to_csv('oneamout.csv', index=False, encoding='utf-8')

print("文件已保存为 oneamount.csv")