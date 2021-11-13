import requests
import json

from src.settings import NV_URL, NV_CLIENT_ID, NV_CLIENT_SECRET
from src.enums import Genre, Country, HttpStatus
from src.utils.field import is_none_or_type, dict_without_none


class APIRequest:
    URL = NV_URL
    CLIENT_ID = NV_CLIENT_ID
    CLIENT_SECRET = NV_CLIENT_SECRET

    def __init__(
        self,
        query: str,
        display: int = None,
        start: int = None,
        genre: str = None,
        country: str = None,
        year_from: int = None,
        year_to: int = None,
    ):
        if not is_none_or_type(display, int):
            raise ValueError(
                "Invalid 'display' value. 'display' should be integer and in range of 1 to 100."
            )
        if not is_none_or_type(start, int):
            raise ValueError(
                "Invalid 'start' value. 'start' should be integer and in range of 1 to 1000"
            )
        if genre and genre.upper() not in Genre.member_names():
            raise ValueError(f"Invalid 'genre' value")
        if country and country not in Country.member_names():
            raise ValueError("Invalid 'country' value.")

        if (year_from is None and year_to is not None) or (
            year_from is not None and year_to is None
        ):
            raise ValueError("year_from and year_to should be used both.")

        self.query = query
        self.display = display
        self.start = start
        self.genre = None if not genre else Genre[genre.upper()].value
        self.country = None if not country else Country(country)
        self.yearfrom = year_from  # noqa
        self.yearto = year_to  # noqa

    def to_dict(self) -> dict:
        return dict_without_none(self.__dict__)

    def to_api(self) -> dict:
        headers = {
            "X-Naver-Client-Id": self.CLIENT_ID,
            "X-Naver-Client-Secret": self.CLIENT_SECRET,
        }
        resp = requests.get(self.URL, headers=headers, params=self.to_dict())
        result = json.loads(resp.content)
        if resp.status_code != HttpStatus.OK.value:
            raise requests.HTTPError(result.get("errorMessage"))

        return result
