import base64
from json import dumps, loads

import faker
from falcon.testing import TestClient
from hamcrest import assert_that, equal_to
from requests import codes

from src.api.src.storage.UsersInfoStorage import UserInfoType
from src.api.tests.constants import USR_URL, USR_INFO_URL
from src.api.tests.functional.utils.auth import create_auth_headers


class TestUserOperations:
    @staticmethod
    def _add_user(client: TestClient, user_info: UserInfoType) -> UserInfoType:
        user_name = user_info.name
        client.simulate_post(USR_URL, body=dumps(dict(user_info)))

        response = client.simulate_get(f"{USR_INFO_URL}/{user_name}")

        assert_that(
            response.status_code, equal_to(codes.ok), f"User {user_name} does not exist"
        )
        return user_info

    def test_delete_user(self, client: TestClient, user_info: UserInfoType):
        user_info = self._add_user(client, user_info)
        user_name = user_info.name

        response = client.simulate_delete(f"/user/{user_name}")

        assert_that(
            response.status_code, equal_to(codes.ok), "Invalid response status code"
        )
        response = client.simulate_get(f"/user_info/{user_name}")
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            f"User {user_name} still exists",
        )

    def test_try_delete_absent_user(self, client: TestClient):
        response = client.simulate_delete(f"{USR_URL}/{faker.Faker().user_name()}")

        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Invalid response status code",
        )

    def test_user_auth(self, client: TestClient, user_info: UserInfoType):
        self._add_user(client, user_info)

        response = client.simulate_get(USR_URL, headers=create_auth_headers(user_info))

        assert_that(response.status_code, equal_to(codes.ok), "User is not authorized")

    def test_user_failed_auth(self, client: TestClient, user_info: UserInfoType):
        user_info = self._add_user(client, user_info)
        creds_txt = f"{user_info.name}:bla"
        creds_encoded = base64.b64encode(creds_txt.encode("utf-8")).decode("utf-8")

        headers = {"Authorization": f"Basic {creds_encoded}"}
        response = client.simulate_get(USR_URL, headers=headers)

        assert_that(
            response.status_code,
            equal_to(codes.unauthorized),
            "Should not be authorized",
        )

    def test_add_user(self, client: TestClient, user_info: UserInfoType):
        response = client.simulate_post(USR_URL, body=dumps(dict(user_info)))

        assert_that(
            response.status_code,
            equal_to(codes.created),
            "Invalid response status code",
        )

    def test_user_exists(self, client: TestClient, user_info: UserInfoType):
        client.simulate_post(USR_URL, body=dumps(dict(user_info)))
        user_name = user_info.name

        response = client.simulate_get(f"{USR_INFO_URL}/{user_name}")

        assert_that(
            response.status_code,
            equal_to(codes.ok),
            f"User {user_name} does not exists",
        )

    def test_try_add_existing_user(self, client: TestClient, user_info: UserInfoType):
        user_info = self._add_user(client, user_info)

        response = client.simulate_post(USR_URL, body=dumps(dict(user_info)))

        assert_that(
            response.status_code,
            equal_to(codes.conflict),
            "Invalid response status code",
        )

    def test_user_absent(self, client: TestClient, user_info: UserInfoType):
        user_name = user_info.name

        response = client.simulate_get(f"{USR_INFO_URL}/{user_name}")

        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            f"User {user_name} DOES exist",
        )

    def test_get_user_info(self, client: TestClient, user_info: UserInfoType):
        user_info = self._add_user(client, user_info)
        user_name = user_info.name

        response = client.simulate_get(f"{USR_INFO_URL}/{user_name}")

        assert_that(
            response.status_code,
            equal_to(codes.ok),
            "Invalid response status code",
        )
        assert_that(
            loads(response.text), equal_to(dict(user_info)), "Invalid user info"
        )

    def test_try_get_absent_user_info(self, client: TestClient):
        response = client.simulate_get(f"{USR_INFO_URL}/{faker.Faker().user_name()}")

        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Invalid response status code",
        )
