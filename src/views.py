from bottle import request

from src import app, movie_recommender
from src.enums import Genre
from src.utils.random_ import rand_letter, rand_word


@app.route("/recommend-movie")
def recommend():
    return movie_recommender.recommend_movie(
        genre=request.query.genre or rand_word(Genre.member_names()),
        query=request.query.query or rand_letter(),
        year_from=request.query.year_from,
        year_to=request.query.year_to,
    ).to_dict()
