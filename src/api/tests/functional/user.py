from json import dumps
from os import getenv

import faker
from hamcrest import assert_that, equal_to
from requests import request, codes
from requests.auth import HTTPBasicAuth

type UserInfo = {
    "name": str,
    "password": str,
    "first_name": str,
    "last_name": str,
    "email": str,
}

BASE_URL = getenv("BASE_URL")
USR_URL = f"{BASE_URL}/user"
USR_INFO_URL = f"{USR_URL}/user_info"


class TestUserOperations:
    @staticmethod
    def _build_usr_info() -> UserInfo:
        return {
            "name": faker.Faker.user_name,
            "password": "test",
            "first_name": faker.Faker.first_name,
            "last_name": faker.Faker.last_name,
        }

    def _add_user(self) -> UserInfo:
        user_info = self._build_usr_info()
        request("POST", USR_URL, data=dumps(user_info))
        user_name = user_info["name"]
        response = request("GET", f"{USR_INFO_URL}/{user_name}")
        assert_that(
            response.status_code, equal_to(codes.ok), "User {user_name} does not exist}"
        )
        return user_info

    def test_add_user(self):
        user_info = self._build_usr_info()
        response = request("POST", USR_URL, data=dumps(user_info))
        assert_that(
            response.status_code, equal_to(codes.ok), "Invalid response status code"
        )

    def test_user_auth(self):
        user_info = self._add_user()
        basic = HTTPBasicAuth(
            username=user_info["name"], password=user_info["password"]
        )
        response = request("GET", f"{USR_URL}/{user_info['name']}", auth=basic)
        assert_that(
            response.status_code, equal_to(codes.ok), "User is not authenticated"
        )

    def test_delete_user(self):
        user_name = self._add_user()

        url = f"{USR_URL}/${user_name}"
        response = request("DELETE", url)
        assert_that(
            response.status_code, equal_to(codes.ok), "Invalid response status code"
        )
        response = request("GET", url)
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            f"User {user_name} still exists",
        )

    def test_user_exists(self):
        user_info = self._build_usr_info()
        request("POST", USR_URL, data=dumps(user_info))
        user_name = user_info["name"]
        response = request("GET", f"{USR_URL}/{user_name}")
        assert_that(
            response.status_code,
            equal_to(codes.ok),
            f"User {user_name} does not exists",
        )

    def test_user_absent(self):
        user_info = self._build_usr_info()
        user_name = user_info["name"]
        response = request("GET", f"{USR_URL}/{user_name}")
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            f"User {user_name} DOES exist",
        )

    def test_try_add_existing_user(self):
        user_info = self._add_user()

        response = request("POST", USR_URL, data=dumps(user_info))
        assert_that(
            response.status_code,
            equal_to(codes.conflict),
            "Invalid response status code",
        )

    def test_try_delete_absent_user(self):
        user_name = self._add_user()

        url = f"{USR_URL}/${user_name}"
        response = request("DELETE", url)
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Invalid response status code",
        )

    def test_get_user_info(self):
        user_name = self._add_user()

        response = request("GET", USR_INFO_URL, params={"username": user_name})

        assert_that(
            response.status_code,
            equal_to(codes.ok),
            "Invalid response status code",
        )
        assert_that(
            response.json(),
            equal_to(
                {
                    "first_name": user_name["first_name"],
                    "last_name": user_name["last_name"],
                }
            ),
            "Invalid user info",
        )

    def test_try_get_absent_user_info(self):
        response = request(
            "GET", USR_INFO_URL, params={"username": faker.Faker.user_name}
        )

        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Invalid response status code",
        )
