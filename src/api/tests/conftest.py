import faker
import pytest
from falcon.testing import TestClient

from src.api.src.app import create_app
from src.api.src.storage.UserInfoType import UserInfoType


@pytest.fixture
def user_info() -> UserInfoType:
    fake = faker.Faker()
    info = {
        "name": fake.user_name(),
        "password": "test",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }
    return UserInfoType(info)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())
