import json
from src.enums import Genre, HttpStatus
from src.git_repo import GithubRepo
from src.request import APIRequest
from src.response import APIResponse
from src.errors import HTTPNotFoundError, HTTPBadRequestError
from src.utils.random_ import rand_letter, rand_int, rand_word


class MovieRecommender:
    REQ_COUNT_LIMIT = 3

    def __init__(self):
        self._gh = GithubRepo()
        self.request_count = 0

    def set_genre_categories(self, genres):
        for genre in genres:
            self._gh.create_genre_label(genre)

    def get_movies(self, genre, query, year_from, year_to):
        try:
            api_resp = APIRequest(
                query=query or rand_letter(),
                start=rand_int(1, 1000),
                display=100,
                genre=genre or rand_word(Genre.member_names()),
                year_from=year_from,
                year_to=year_to,
            ).to_api()
        except Exception as e:
            raise HTTPBadRequestError(str(e))

        content = json.loads(api_resp.content)

        if api_resp.status_code == HttpStatus.NOT_FOUND.value:
            raise HTTPNotFoundError(content.get("errorMessage"))

        resp_obj = APIResponse.from_api(**content)
        if not resp_obj.items:
            if self.request_count == self.REQ_COUNT_LIMIT:
                raise RuntimeError("There is no matched movie.")
            self.request_count += 1
            return self.get_movies(genre, query, year_from, year_to)

        return sorted(resp_obj.items, key=lambda k: k.user_rating, reverse=True)

    def recommend_movie(self, genre, query, year_from, year_to):
        movies = self.get_movies(genre, query, year_from, year_to)
        return movies[0]
