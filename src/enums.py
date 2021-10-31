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
    DRAMA = auto()
    FANTASY = auto()
    WESTERN = auto()
    HORROR = auto()
    ROMANCE = auto()
    ADVENTURE = auto()
    THRILLER = auto()
    NOIR = auto()
    CULT = auto()
    DOCUMENTARY = auto()
    COMEDY = auto()
    FAMILY = auto()


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
