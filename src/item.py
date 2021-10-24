from src.utils import dict_fields_to_snake_case


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
        user_rating: int,
    ):
        self.title = title
        self.link = link
        self.image = image
        self.subtitle = subtitle
        self.pub_date = pub_date
        self.director = director
        self.actor = actor
        self.user_rating = user_rating

    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_obj(cls, **kwargs):
        return cls(**dict_fields_to_snake_case(kwargs))

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
