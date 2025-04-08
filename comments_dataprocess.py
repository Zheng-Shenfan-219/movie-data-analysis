'''
针对原始的comment数据，重构为comments_data表.
'''
import pandas as pd
from data_process import run_comments_check

dataset = './dataset/comment.xlsx'
df = pd.read_excel(dataset)
new_df = pd.DataFrame()
new_df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
new_df['name'] = df['name'].astype(str)
new_df['post_time'] = pd.to_datetime(df['date'], format='%Y/%m/%d %H:%M', errors='coerce')
new_df['number_likes'] = pd.to_numeric(df['number_likes'], errors='coerce')
new_df['recommend'] = df['recommend'].astype(str)
new_df['comment'] = df['comment'].astype(str)

# 检查所有的列
original_rows = len(new_df)
mask = run_comments_check(new_df)
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
        csv_file = './dataset/processed/comments_data.csv'
        filtered_df.to_csv(csv_file, index=False, encoding='utf-8-sig') 
        print(f"已将过滤后的数据保存到 {csv_file}")
    except Exception as e:
        print(f"保存CSV文件时发生错误: {str(e)}")