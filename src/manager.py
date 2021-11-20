from src.enums import Genre
from src.git_repo import GithubRepo
from src.request import APIRequest
from src.response import APIResponse
from src.utils.random_ import rand_letter, rand_int, rand_word


class CommandManager:
    RECOMMEND_LIMIT = 3

    def __init__(self):
        self._gh = GithubRepo()
        self.recommend_count = 0

    def set_genre_categories(self, genres):
        for genre in genres:
            self._gh.create_genre_label(genre)

    @staticmethod
    def reset_env(client_id, client_secret, github_access_token, github_repo):
        with open(".env", "w") as env_file:
            env_file.write("NV_URL=https://openapi.naver.com/v1/search/movie\n")
            env_file.write(f"NV_CLIENT_ID={client_id}\n")
            env_file.write(f"NV_CLIENT_SECRET={client_secret}\n")
            env_file.write(f"GITHUB_ACCESS_TOKEN={github_access_token}\n")
            env_file.write(f"GITHUB_REPO={github_repo}\n")

    def get_movies(self, genre, query, year_from, year_to):
        api_result = APIRequest(
            query=query or rand_letter(),
            start=rand_int(1, 1000),
            display=100,
            genre=genre or rand_word(Genre.member_names()),
            year_from=year_from,
            year_to=year_to,
        ).to_api()

        resp = APIResponse.from_api(**api_result)
        if not resp.items:
            if self.recommend_count < self.RECOMMEND_LIMIT:
                raise RuntimeError("There is no matched movie.")
            self.recommend_count += 1
            return self.get_movies(genre, query, year_from, year_to)

        return sorted(resp.items, key=lambda k: k.user_rating, reverse=True)

    def recommend_movie(self, genre, query, year_from, year_to):
        movies = self.get_movies(genre, query, year_from, year_to)
        return movies[0]
