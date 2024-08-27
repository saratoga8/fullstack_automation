from json import dumps, loads
from os import getenv

import faker
import pytest
from hamcrest import assert_that, equal_to
from requests import request, codes
from requests.auth import HTTPBasicAuth
from storage.UsersInfoStorage import UserInfoType

BASE_URL = getenv("BASE_URL")
USR_URL = f"{BASE_URL}/user"
USR_INFO_URL = f"{BASE_URL}/user_info"


class TestUserOperations:
    @staticmethod
    def _build_usr_info() -> UserInfoType:
        fake = faker.Faker()
        return {
            "name": fake.user_name(),
            "password": "test",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }

    def _add_user(self) -> UserInfoType:
        user_info = self._build_usr_info()
        request("POST", USR_URL, data=dumps(user_info))
        user_name = user_info["name"]
        response = request("GET", f"{USR_INFO_URL}/{user_name}")
        assert_that(
            response.status_code, equal_to(codes.ok), f"User {user_name} does not exist"
        )
        return user_info

    def test_delete_user(self):
        user_info = self._add_user()
        user_name = user_info["name"]

        response = request("DELETE", f"{USR_URL}/{user_name}")
        assert_that(
            response.status_code, equal_to(codes.ok), "Invalid response status code"
        )
        response = request("GET", f"{USR_INFO_URL}/{user_name}")
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            f"User {user_name} still exists",
        )

    def test_try_delete_absent_user(self):
        response = request("DELETE", f"{USR_URL}/{faker.Faker().user_name()}")
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Invalid response status code",
        )

    @pytest.mark.current
    def test_user_auth(self):
        user_info = self._add_user()
        user_name = user_info["name"]
        basic = HTTPBasicAuth(user_name, user_info["password"])
        response = request("GET", f"{USR_URL}", auth=basic)
        assert_that(
            response.status_code, equal_to(codes.ok), "User is not authenticated"
        )

    def test_add_user(self):
        user_info = self._build_usr_info()
        response = request("POST", USR_URL, data=dumps(user_info))
        assert_that(
            response.status_code,
            equal_to(codes.created),
            "Invalid response status code",
        )

    def test_user_exists(self):
        user_info = self._build_usr_info()
        request("POST", USR_URL, data=dumps(user_info))
        user_name = user_info["name"]
        response = request("GET", f"{USR_INFO_URL}/{user_name}")
        assert_that(
            response.status_code,
            equal_to(codes.ok),
            f"User {user_name} does not exists",
        )

    def test_try_add_existing_user(self):
        user_info = self._add_user()

        response = request("POST", USR_URL, data=dumps(user_info))
        assert_that(
            response.status_code,
            equal_to(codes.conflict),
            "Invalid response status code",
        )

    def test_user_absent(self):
        user_info = self._build_usr_info()
        user_name = user_info["name"]
        response = request("GET", f"{USR_INFO_URL}/{user_name}")
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            f"User {user_name} DOES exist",
        )

    def test_get_user_info(self):
        user_info = self._add_user()
        user_name = user_info["name"]

        response = request("GET", f"{USR_INFO_URL}/{user_name}")

        assert_that(
            response.status_code,
            equal_to(codes.ok),
            "Invalid response status code",
        )
        assert_that(loads(response.text), equal_to(user_info), "Invalid user info")

    def test_try_get_absent_user_info(self):
        response = request("GET", f"{USR_INFO_URL}/{faker.Faker().user_name()}")

        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Invalid response status code",
        )
