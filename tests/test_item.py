import pytest

from src.item import Item


@pytest.fixture
def item(fake):
    return Item(
        title=fake.word(),
        link=fake.domain_name(),
        image=fake.domain_name(),
        subtitle=fake.sentence(),
        pub_date=str(fake.date_time()),
        director=fake.name(),
        actor=fake.name(),
        user_rating=fake.pyfloat(right_digits=2, min_value=0, max_value=10),
    )


def test_get_obj_should_return_item_instance(item):
    kwargs = item.to_dict()
    instance = Item.get_obj(**kwargs)
    assert isinstance(instance, Item)
    assert instance.title == kwargs["title"]
    assert instance.link == kwargs["link"]
    assert instance.image == kwargs["image"]
    assert instance.subtitle == kwargs["subtitle"]
    assert instance.pub_date == kwargs["pub_date"]
    assert instance.director == kwargs["director"]
    assert instance.actor == kwargs["actor"]
    assert instance.user_rating == kwargs["user_rating"]


def test_markdown_should_include_item_info(item):
    md_txt = item.markdown_text

    assert item.title in md_txt
    assert item.link in md_txt
    assert item.pub_date in md_txt
    assert item.image in md_txt
    assert item.subtitle in md_txt
    assert item.director in md_txt
    assert item.actor in md_txt
    assert str(item.user_rating) in md_txt
