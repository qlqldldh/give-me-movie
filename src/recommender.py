import json

from bottle import HTTPError

from src.enums import HttpStatus
from src.request import APIRequest
from src.response import APIResponse
from src.item import Item
from src.utils.random_ import rand_int


class MovieRecommender:
    REQ_COUNT_LIMIT = 3

    def __init__(self):
        self.__request_count = 0

    def get_movies(self, **kwargs) -> list[dict]:
        start = rand_int(1, 1000)
        display = 100
        resp = self._get_resp_from_api(start=start, display=display, **kwargs)

        if not resp.items:
            if self.__request_count == self.REQ_COUNT_LIMIT:
                raise HTTPError(
                    status=HttpStatus.NOT_FOUND.value, body="There is no matched movie."
                )
            self.__request_count += 1
            return self.get_movies(**kwargs)

        return sorted(resp.items, key=lambda k: k.user_rating, reverse=True)

    def recommend_movie(self, **kwargs) -> Item:
        movies = self.get_movies(**kwargs)
        return movies[0]  # TODO: apply recommendation algorithm

    @staticmethod
    def _get_resp_from_api(**kwargs) -> APIResponse:
        try:
            api_resp = APIRequest(**kwargs).to_api()
        except Exception as e:
            raise HTTPError(status=HttpStatus.BAD_REQUEST.value, body=str(e))

        content = json.loads(api_resp.content)
        if api_resp.status_code != HttpStatus.OK.value:
            raise HTTPError(
                status=api_resp.status_code, body=content.get("errorMessage")
            )

        return APIResponse.from_api(**content)
