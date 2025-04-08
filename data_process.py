import pandas as pd
import numpy as np
from typing import List, Any
from datetime import datetime
import ast

def convert_to_list(x):
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        try:
            # 将字符串解析为列表
            return ast.literal_eval(x)
        except Exception as e:
            return x.split()
    return []

def check_id(df: pd.DataFrame) -> pd.Series:
    return (df['ID'].notna() &
            (df['ID'].dtype == 'int64') &
            df['ID'].duplicated().apply(lambda x: not x) &
            (df['ID'] > 0))

def check_comments_id(df: pd.DataFrame) -> pd.Series:
    return (df['ID'].notna() &
            (df['ID'].dtype == 'int64') &
            (df['ID'] > 0))

def check_name(df: pd.DataFrame) -> pd.Series:
    return (df['name'].notna() &
            (df['name'].dtype == 'object') &
            (df['name'].str.len() > 0) &
            (df['name'].str.len() < 100))

def check_released_date(df: pd.DataFrame) -> pd.Series:
    current_year = pd.Timestamp.now().year
    return (df['released_date'].notna() &
            (df['released_date'].dtype == 'int64') &
            (df['released_date'] >= 1900) &
            (df['released_date'] <= current_year))

def check_tags(df: pd.DataFrame) -> pd.Series:
    return (df['tags'].apply(lambda x: isinstance(x, list) and len(x) > 0))

def check_area(df: pd.DataFrame) -> pd.Series:
    allowed_areas = ["中国大陆", "中国台湾", "中国香港"]
    return (df['area'].apply(lambda areas: isinstance(areas, list) and
                             len(areas) > 0 and
                             all(area in allowed_areas for area in areas)))

def check_director(df: pd.DataFrame) -> pd.Series:
    return (df['director'].apply(lambda x: isinstance(x, list) and
                                 len(x) > 0 and
                                 len(x) == len(set(x))))

def check_actor(df: pd.DataFrame) -> pd.Series:
    return (df['actor'].apply(lambda x: isinstance(x, list) and
                              len(x) > 0 and
                              len(x) == len(set(x))))

def check_post_time(df: pd.DataFrame) -> pd.Series:
    def is_valid_datetime(x):
        if isinstance(x, pd.Timestamp):
            # 如果已经是Timestamp对象，直接检查年份范围
            return 1900 <= x.year <= datetime.now().year
        elif isinstance(x, str):
            try:
                dt = datetime.strptime(x, "%Y/%m/%d %H:%M")
                return 1900 <= dt.year <= datetime.now().year
            except ValueError:
                return False
        else:
            return False
    
    return df['post_time'].apply(is_valid_datetime)

def check_recommend(df: pd.DataFrame) -> pd.Series:
    valid_recommendations = ['力荐', '推荐', '还行', '较差', '很差']
    return (df['recommend'].notna() &
            df['recommend'].isin(valid_recommendations))

def check_number_likes(df: pd.DataFrame) -> pd.Series:
    return (df['number_likes'].notna() &
            (df['number_likes'].dtype == 'int64') &
            (df['number_likes'] >= 0))

def check_comment(df: pd.DataFrame) -> pd.Series:
    return (df['comment'].notna() &
            (df['comment'].dtype == 'object') &
            (df['comment'].str.len() > 0))


def run_comments_check(df: pd.DataFrame) -> pd.Series:
    return (check_comments_id(df) &
            check_name(df) &
            check_post_time(df) &
            check_recommend(df) &
            check_number_likes(df) &
            check_comment(df) )

def run_films_check(df: pd.DataFrame) -> pd.Series:
    return (check_id(df) &
            check_name(df) &
            check_released_date(df) &
            check_tags(df) &
            check_area(df) &
            check_director(df) &
            check_actor(df))
