import csv
import os
from collections import defaultdict


def split_csv_standard(input_file, group_column, output_folder='output'):
    """
    使用标准库按列分组CSV文件
    """
    os.makedirs(output_folder, exist_ok=True)

    # 读取数据并分组
    groups = defaultdict(list)

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            group_value = row[group_column]
            groups[group_value].append(row)

    # 写入分组文件
    for group_value, rows in groups.items():
        safe_name = str(group_value).replace('/', '_').replace('\\', '_').replace(':', '_')
        filename = f"bill_{safe_name}.csv"
        filepath = os.path.join(output_folder, filename)

        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"已创建: {filename}，记录数: {len(rows)}")

    print(f"\n完成！共生成 {len(groups)} 个文件")


# 使用
split_csv_standard('BOSS.csv', 'bills_id')