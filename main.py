from bottle import run

from src.views import app as movie_app
from src.settings import SERVER_HOST, SERVER_PORT


if __name__ == "__main__":
    run(
        app=movie_app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=False,
    )
