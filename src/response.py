from src.utils.field import dict_fields_to_snake_case
from src.item import Item


class APIResponse:
    def __init__(
        self,
        last_build_date: str,
        total: int,
        start: int,
        display: int,
        items: list[dict],
    ):
        self.last_build_date = last_build_date
        self.total = total
        self.start = start
        self.display = display
        self.items = [Item.get_obj(**item) for item in items]

    @classmethod
    def from_api(cls, **kwargs):
        return cls(**dict_fields_to_snake_case(kwargs))
