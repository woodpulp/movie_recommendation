from flask import Flask, render_template, request
import models
import models02

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = request.form.get('user_id')
    recommendations = models.get_recommendations(user_id)
    return render_template('recommendations.html', user_id=user_id, recommendations=recommendations)

@app.route('/top100')
def top100():
    top_movies = models02.get_top_n_movies_by_average_rating(100)
    return render_template('top100.html', top_movies=top_movies)

@app.route('/genre_recommendations')
def genre_recommendations():
    genre = request.args.get('genre', '')
    if not genre:
        return "请输入有效的电影类型"
    genre_movies = models02.movies_df[models02.movies_df['Genres'].str.contains(genre, na=False)]['Title'].tolist()
    return render_template('genre_recommendations.html', genre_movies=genre_movies)


if __name__ == '__main__':
    app.run(debug=True)
