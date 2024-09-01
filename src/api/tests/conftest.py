import faker
import pytest

from src.storage.UserInfoType import UserInfoType


@pytest.fixture(scope="function")
def user_info() -> UserInfoType:
    fake = faker.Faker()
    info = {
        "name": fake.user_name(),
        "password": "test",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }
    return UserInfoType(info)
