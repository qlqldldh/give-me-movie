import pytest

from src.item import Item
from tests.mocks.factories import ItemFactory


@pytest.fixture
def item(fake):
    return ItemFactory()


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
