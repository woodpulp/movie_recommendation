import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from collections import defaultdict

# 数据加载
movies = pd.read_csv('data/movies.csv', sep='::', header=None, names=['movie_id', 'title', 'genres'], engine='python')
ratings_files = ['data/ratings_1.txt', 'data/ratings_2.txt', 'data/ratings_3.txt', 'data/ratings_4.txt',
                 'data/ratings_5.txt']
ratings = pd.concat(
    [pd.read_csv(f, sep='::', header=None, names=['user_id', 'movie_id', 'rating', 'timestamp'], engine='python') for f
     in ratings_files]
)

# 创建 Surprise 数据集
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['user_id', 'movie_id', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

# 训练模型
algo = SVD()
algo.fit(trainset)


# 获取推荐电影
def get_recommendations(user_id, top_n=10):
    user_id = int(user_id)
    # 获取用户已经评分过的电影
    user_ratings = ratings[ratings['user_id'] == user_id]

    if user_ratings.empty:
        return ["No recommendations found for this user."]

    # 获取所有电影的ID
    all_movie_ids = ratings['movie_id'].unique()
    # 获取用户还没有评分过的电影
    movies_not_rated = [movie_id for movie_id in all_movie_ids if movie_id not in user_ratings['movie_id'].values]

    # 预测用户对这些电影的评分
    predictions = [algo.predict(user_id, movie_id) for movie_id in movies_not_rated]

    # 按预测评分排序
    sorted_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)

    # 获取前 top_n 个推荐电影的ID
    top_movie_ids = [pred.iid for pred in sorted_predictions[:top_n]]

    # 获取这些电影的标题
    recommended_movies = movies[movies['movie_id'].isin(top_movie_ids)]
    return recommended_movies['title'].tolist()
