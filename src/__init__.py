from bottle import Bottle
from src.manager import MovieRecommender

app = Bottle()
movie_recommender = MovieRecommender()
