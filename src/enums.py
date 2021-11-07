from enum import auto, Enum


class EnumClass(Enum):
    @classmethod
    def member_names(cls) -> list:
        return cls.__dict__.get("_member_names_")

    @classmethod
    def is_valid_value(cls, value: str) -> bool:
        if isinstance(value, str):
            return value in cls.member_names()


class Genre(EnumClass):
    DRAMA = 1
    FANTASY = 2
    WESTERN = 3
    HORROR = 4
    ROMANCE = 5
    ADVENTURE = 6
    THRILLER = 7
    NOIR = 8
    CULT = 9
    DOCUMENTARY = 10
    COMEDY = 11
    FAMILY = 12


class Country(EnumClass):
    KR = auto()
    JP = auto()
    US = auto()
    HK = auto()
    GB = auto()
    FR = auto()
    ETC = auto()


class HttpStatus(Enum):
    OK = 200
    NOT_FOUND = 404
    BAD_REQUEST = 400
    SERVER_ERROR = 500
