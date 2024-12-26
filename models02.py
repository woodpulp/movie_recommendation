import pandas as pd

# 加载数据和数据预处理
# 加载电影信息
movies_df = pd.read_csv('data/movies.csv', sep='::', header=None, names=['MovieID', 'Title', 'Genres'], engine='python')
# 提取年份，这里假设年份总是跟在括号内，并且格式正确
movies_df['Year'] = movies_df['Title'].apply(
    lambda x: int(''.join(filter(str.isdigit, x.split('(')[-1]))) if '(' in x else None)

# 加载所有评分数据
ratings_dfs = []
for i in range(1, 6):
    ratings_df = pd.read_csv(f'data/ratings_{i}.txt', sep='::', header=None,
                             names=['UserID', 'MovieID', 'Rating', 'Timestamp'], engine='python')
    ratings_df['UserID'] = ratings_df['UserID'].astype(str)
    ratings_df['Timestamp'] = ratings_df['Timestamp'].astype(str)
    ratings_dfs.append(ratings_df)
ratings_df = pd.concat(ratings_dfs, ignore_index=True)

# 合并电影信息和评分数据
merged_df = movies_df.merge(ratings_df, on='MovieID', how='left')

# 按照MovieID排序
merged_df.sort_values(by='MovieID', inplace=True)

# 保存排序后的合并数据到CSV文件
merged_df.to_csv('merged_sorted.csv', index=False)

# 计算每个电影的平均评分
average_ratings = ratings_df.groupby('MovieID')['Rating'].mean().reset_index()
average_ratings.rename(columns={'Rating': 'AverageRating'}, inplace=True)
movies_df = movies_df.merge(average_ratings, on='MovieID', how='left')

# 填充缺失的平均评分（如果有的话）
movies_df['AverageRating'].fillna(0, inplace=True)


# 获取评分最高的100部电影
def get_top_n_movies_by_average_rating(top_n=100):
    top_movies_df = movies_df.sort_values(by='AverageRating', ascending=False).head(top_n)
    # 返回电影标题和平均评分
    top_movies = top_movies_df[['Title', 'AverageRating']].values.tolist()
    return top_movies


