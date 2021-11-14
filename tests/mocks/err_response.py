import json
from faker import Faker

fake = Faker()


class MockErrResp:
    def __init__(self, status_code):
        self._status_code = status_code

    @property
    def content(self):
        return json.dumps({"errMessage": fake.sentence()})

    @property
    def status_code(self):
        return self._status_code
