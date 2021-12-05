from uuid import uuid4
import pytest

from src.item import Item
from tests.mocks.factories import ItemFactory

from src.manager import MovieRecommender
from src.enums import Genre
from src.utils.random_ import rand_letter


@pytest.fixture
def cmd_manager():
    return MovieRecommender()


@pytest.fixture
def env_vars(fake):
    return {
        "client_id": str(uuid4()),
        "client_secret": str(uuid4()),
        "github_access_token": str(uuid4()),
        "github_repo": f"{fake.last_name()}/{fake.word()}",
    }


@pytest.fixture
def env_vars_content(env_vars):
    return (
        f"NV_URL=https://openapi.naver.com/v1/search/movie\n"
        f"NV_CLIENT_ID={env_vars['client_id']}\n"
        f"NV_CLIENT_SECRET={env_vars['client_secret']}\n"
        f"GITHUB_ACCESS_TOKEN={env_vars['github_access_token']}\n"
        f"GITHUB_REPO={env_vars['github_repo']}\n"
    )


@pytest.fixture
def api_result(fake, request):
    return {
        "last_build_date": str(fake.date_time()),
        "total": fake.pyint(),
        "start": fake.pyint(),
        "display": fake.pyint(),
        "items": request.param,
    }


def test_reset_env_should_write_env_file(
    mocker, cmd_manager, env_vars, env_vars_content
):
    mocker.patch("builtins.open", mocker.mock_open(read_data=env_vars_content))
    cmd_manager.reset_env(**env_vars)

    with open(".env", "r") as env_file:
        assert "NV_URL" in env_file.readline()
        for env_info in env_vars.values():
            assert env_info in env_file.readline()


@pytest.mark.parametrize("api_result", [list()], indirect=True)
def test_get_movies_should_raise_exception_when_no_movie_found(
    fake, mocker, cmd_manager, api_result
):
    mocker.patch("src.request.APIRequest.to_api", return_value=api_result)
    with pytest.raises(RuntimeError):
        cmd_manager.get_movies(
            genre=fake.word(ext_word_list=Genre.member_names()),
            query=rand_letter(),
            year_from=fake.pyint(min_value=1987, max_value=2021),
            year_to=fake.pyint(min_value=1987, max_value=2021),
        )


@pytest.mark.parametrize(
    "api_result",
    [
        [item.to_dict() for item in ItemFactory.create_batch(10)],
    ],
    indirect=True,
)
def test_get_movies_should_return_rate_sorted_movies(
    mocker, fake, cmd_manager, api_result
):
    mocker.patch("src.request.APIRequest.to_api", return_value=api_result)
    movies = cmd_manager.get_movies(
        genre=fake.word(ext_word_list=Genre.member_names()),
        query=rand_letter(),
        year_from=fake.pyint(min_value=1987, max_value=2021),
        year_to=fake.pyint(min_value=1987, max_value=2021),
    )

    assert isinstance(movies, list)
    assert all(isinstance(movie, Item) for movie in movies)
    assert all(
        movies[i].user_rating >= movies[i + 1].user_rating
        for i in range(len(movies) - 1)
    )


@pytest.mark.parametrize(
    "api_result",
    [
        [item.to_dict() for item in ItemFactory.create_batch(10)],
    ],
    indirect=True,
)
def test_recommend_movie_should_return_item_instance(
    mocker, fake, cmd_manager, api_result
):
    mocker.patch("src.request.APIRequest.to_api", return_value=api_result)
    movie = cmd_manager.recommend_movie(
        genre=fake.word(ext_word_list=Genre.member_names()),
        query=rand_letter(),
        year_from=fake.pyint(min_value=1987, max_value=2021),
        year_to=fake.pyint(min_value=1987, max_value=2021),
    )

    assert isinstance(movie, Item)
    assert all(
        movie.user_rating >= item.get("user_rating") for item in api_result["items"]
    )
