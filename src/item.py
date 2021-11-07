from typing import Union

from typer import echo, style
from typer.colors import BLACK, BRIGHT_YELLOW, BRIGHT_RED

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
        self.subtitle = subtitle
        self.pub_date = pub_date
        self.director = replace_to_comma(director)  # 망할 네이버..
        self.actor = replace_to_comma(actor)  # 망할 네이버..
        self.user_rating = float(user_rating)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_obj(cls, **kwargs):
        return cls(**dict_fields_to_snake_case(kwargs))

    def show(self):
        echo(f"Title: {style(self.title, fg=BLACK, bg=BRIGHT_YELLOW)}")
        echo(f"Director: {self.director}")
        echo(f"Actors: {self.actor}")
        echo(f"Rate: {style(self.user_rating, fg=BRIGHT_RED)}")

    @property
    def markdown_text(self):
        return f"""
        # {self.title}
        
        > link: {self.link}
        
        > published: {self.pub_date}
        
        <p align="center">
            <img width="330" height="471" src="{self.image}"><br>
            {self.subtitle}
        </p>
        
        - Director: {self.director}
        
        - Actors: {self.actor}
        
        - User Rating: {self.user_rating}
        
        """
