from faker import Faker
import pytest


@pytest.fixture(scope="session")
def fake():
    return Faker()
