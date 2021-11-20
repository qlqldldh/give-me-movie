from factory import Factory, Faker

from src.item import Item


class ItemFactory(Factory):
    class Meta:
        model = Item

    title = Faker("word")
    link = Faker("domain_name")
    image = Faker("domain_name")
    subtitle = Faker("sentence")
    pub_date = str(Faker("date_time"))
    director = Faker("name")
    actor = Faker("name")
    user_rating = Faker("pyfloat", right_digits=2, min_value=0, max_value=10)
