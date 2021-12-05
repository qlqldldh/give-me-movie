from bottle import request

from src import app, movie_recommender


@app.route("/recommend-movie")
def recommend():
    return movie_recommender.recommend_movie(
        request.query.genre,
        request.query.query,
        request.query.year_from,
        request.query.year_to,
    ).to_dict()
