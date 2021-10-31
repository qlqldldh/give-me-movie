from typing import Union

import typer
from src.utils import dict_fields_to_snake_case, remove_bold_exp


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
        self.director = director.replace("|", ",")[:-1]  # 망할 네이버..
        self.actor = actor.replace("|", ",")[:-1]  # 망할 네이버..
        self.user_rating = float(user_rating)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_obj(cls, **kwargs):
        return cls(**dict_fields_to_snake_case(kwargs))

    def echo(self):
        typer.echo(f"Title: {typer.style(self.title, fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_YELLOW)}")
        typer.echo(f"Director: {self.director}")
        typer.echo(f"Actors: {self.actor}")
        typer.echo(f"Rate: {typer.style(self.user_rating, fg=typer.colors.BRIGHT_RED)}")

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
