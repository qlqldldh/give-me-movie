from typing import Union

from src.utils.field import dict_fields_to_snake_case, remove_bold_exp, replace_to_comma


class Item:
    def __init__(
        self,
        title: str,
        link: str,
        image: str,
        subtitle: str,
        pub_date: str,
        director: str,
        actor: str,
        user_rating: Union[float, str],
    ):
        self.title = remove_bold_exp(title)  # 망할 네이버..
        self.link = link
        self.image = image
        self.subtitle = remove_bold_exp(subtitle)
        self.pub_date = pub_date
        self.director = replace_to_comma(director)  # 망할 네이버..
        self.actor = replace_to_comma(actor)  # 망할 네이버..
        self.user_rating = float(user_rating)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_obj(cls, **kwargs):
        return cls(**dict_fields_to_snake_case(kwargs))
