from faker import Faker

from src.response import APIResponse


def test_from_api_should_return_response_instance():
    fake = Faker()
    kwargs = {
        "last_build_date": str(fake.date_time()),
        "total": fake.pyint(),
        "start": fake.pyint(),
        "display": fake.pyint(max_value=100),
        "items": [],
    }

    assert isinstance(APIResponse.from_api(**kwargs), APIResponse)
