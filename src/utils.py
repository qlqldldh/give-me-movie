import re
from typing import Any


def is_none_or_type(target: Any, type_: Any):
    return target is None or isinstance(target, type_)


def pascal_to_snake_case(field: str) -> str:
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", field).lower()


def dict_fields_to_snake_case(obj: dict) -> dict:
    return {pascal_to_snake_case(key): value for key, value in obj.items()}


def dict_without_none(obj: dict) -> dict:
    return {key: value for key, value in obj.items() if value}
