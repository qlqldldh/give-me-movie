import pytest
from requests import HTTPError
from faker import Faker
from string import ascii_letters

from src.request import APIRequest
from src.enums import Country, Genre, HttpStatus

from tests.mocks.err_response import MockErrResp


@pytest.fixture
def api_req_kwargs(fake):
    return {
        "query": fake.word(ext_word_list=list(ascii_letters)),
        "display": fake.pyint(),
        "start": fake.pyint(),
        "genre": fake.word(ext_word_list=Genre.member_names()),
        "country": fake.word(ext_word_list=Country.member_names()),
        "year_from": fake.year(),
        "year_to": fake.year(),
    }


@pytest.fixture(
    params=[status for status in HttpStatus.member_names() if status != "OK"]
)
def mocked_err_response(request):
    return MockErrResp(request.param)


@pytest.fixture
def invalid_genre(fake):
    genre = fake.word()
    while genre.upper() in Genre.member_names():
        genre = fake.word()

    return genre


@pytest.mark.parametrize(
    "invalid_display",
    [
        2.5,  # float
        "display",  # string
    ],
)
def test_init_with_not_int_display_should_raise_exception(fake, invalid_display):
    with pytest.raises(ValueError):
        APIRequest(fake.word(), invalid_display)  # noqa


@pytest.mark.parametrize(
    "invalid_start",
    [
        2.5,  # float
        "start",  # string
    ],
)
def test_init_with_not_int_start_should_raise_exception(fake, invalid_start):
    with pytest.raises(ValueError):
        APIRequest(fake.word(), fake.pyint(), invalid_start)  # noqa


def test_init_with_invalid_genre_should_raise_exception(fake, invalid_genre):
    with pytest.raises(ValueError):
        APIRequest(query=fake.word(), genre=invalid_genre)


def test_inti_with_invalid_country_should_raise_exception(fake):
    invalid_country = fake.word()
    with pytest.raises(ValueError):
        APIRequest(query=fake.word(), country=invalid_country)


@pytest.mark.parametrize(
    "year_from, year_to",
    [
        (str(Faker().date_time()), None),  # year_from is not None, year_to is None
        (None, str(Faker().date_time())),  # year_from is None, year_to is not None
    ],
)
def test_init_with_invalid_year_from_year_to_should_raise_exception(
    fake, year_from, year_to
):
    with pytest.raises(ValueError):
        APIRequest(query=fake.word(), year_from=year_from, year_to=year_to)


@pytest.mark.parametrize(
    "field",
    [
        "display",
        "start",
        "genre",
        "country",
    ],
)
def test_to_dict_should_return_dict_without_none_value(api_req_kwargs, field):
    api_req_kwargs.update({field: None})
    req = APIRequest(**api_req_kwargs)
    result = req.to_dict()

    assert result.get(field) is None
