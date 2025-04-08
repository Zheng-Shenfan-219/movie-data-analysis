'''
针对原始的data数据，重构为films_data表.
'''
import pandas as pd
import ast
from data_process import run_films_check,convert_to_list

dataset = './dataset/data.xlsx'
df = pd.read_excel(dataset)
# 重构subtitle列
split_cols = df['card_subtitle'].str.split('/', expand=True)
# 去除每个部分的多余空白字符
split_cols = split_cols.apply(lambda col: col.str.strip())

# 重构后的表格
new_df = pd.DataFrame()
new_df['ID'] = pd.to_numeric(df['id'], errors='coerce')
new_df['name'] = df['name'].astype(str)
new_df['director'] = df['director'].apply(convert_to_list)
new_df['actor'] = df['actor'].apply(convert_to_list)
new_df['released_date'] = pd.to_numeric(split_cols[0], errors='coerce')
new_df['tags'] = split_cols[2].apply(lambda x: [tag for tag in x.split() if tag] if isinstance(x, str) else [])
new_df['area'] = split_cols[1].apply(lambda x: [tag for tag in x.split() if tag] if isinstance(x, str) else [])
# 检查所有的列
original_rows = len(new_df)
mask = run_films_check(new_df)
filtered_df = new_df[mask]

# 计算并打印被移除的行数
removed_rows = original_rows - len(filtered_df)
print(f"原始数据行数: {original_rows}")
print(f"移除的行数: {removed_rows}")
print(f"保留的行数: {len(filtered_df)}")
# 输出新表结果预览
print("\n重构后的数据预览：")
print(filtered_df.head())

# 检查filtered_df是否为空
if filtered_df.empty:
    print("过滤后的数据为空")
else:
    # 保存为CSV文件
    try:
        csv_file = './dataset/processed/films_data.csv'
        filtered_df.to_csv(csv_file, index=False, encoding='utf-8-sig') 
        print(f"已将过滤后的数据保存到 {csv_file}")
    except Exception as e:
        print(f"保存CSV文件时发生错误: {str(e)}")



