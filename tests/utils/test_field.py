import pytest
from faker import Faker

from src.utils.field import (
    is_none_or_type,
    pascal_to_snake_case,
    dict_fields_to_snake_case,
    dict_without_none,
    remove_bold_exp,
    replace_to_comma,
)


@pytest.mark.parametrize(
    "target, type_, expected",
    [
        (None, str, True),
        (None, int, True),
        (Faker().word(), str, True),
        (Faker().word(), int, False),
    ],
)
def test_is_none_or_type(target, type_, expected):
    assert is_none_or_type(target, type_) == expected


@pytest.mark.parametrize(
    "field, expected",
    [
        ("ParamCase", "param_case"),
        ("paramCase", "param_case"),
    ],
)
def test_pascal_to_snake_case(field, expected):
    assert pascal_to_snake_case(field) == expected


def test_dict_fields_to_snake_case():
    obj = {"KeyValue": "key_value", "PascalCase": "pascal_case_value"}
    expected = {"key_value": "key_value", "pascal_case": "pascal_case_value"}
    assert dict_fields_to_snake_case(obj) == expected


def test_dict_without_none():
    obj = {"key": "value1", "key_with_none_value": None}
    expected = {"key": "value1"}
    assert dict_without_none(obj) == expected


def test_remove_bold_exp():
    expected = Faker().word()
    s = f"<b>{expected}</b>"
    assert remove_bold_exp(s) == expected


def test_replace_to_comma():
    s = "데이지 리들리|마크 해밀|오스카 아이삭|아담 드라이버|캐리 피셔|존 보예가|"
    expected = "데이지 리들리,마크 해밀,오스카 아이삭,아담 드라이버,캐리 피셔,존 보예가"
    assert replace_to_comma(s) == expected
