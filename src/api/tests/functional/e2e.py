from json import dumps, loads

from falcon.testing import TestClient
from hamcrest import assert_that, equal_to
from requests import codes

from src.api.src.storage.UsersInfoStorage import UserInfoType
from src.api.tests.constants import USR_URL, USR_INFO_URL
from src.api.tests.functional.utils.auth import create_auth_headers


class TestE2E:
    def test_e2e(self, client: TestClient, user_info: UserInfoType):
        user_name = user_info.name
        auth_headers = create_auth_headers(user_info)
        user_info_dict = dict(user_info)

        client.simulate_post(USR_URL, body=dumps(user_info_dict))

        response = client.simulate_get(USR_URL, headers=auth_headers)
        assert_that(response.status_code, equal_to(codes.ok), "User is not authorized")

        response = client.simulate_get(f"{USR_INFO_URL}/{user_name}")
        assert_that(
            response.status_code, equal_to(codes.ok), "User info is not retrieved"
        )
        assert_that(loads(response.text), equal_to(user_info_dict), "Invalid user info")

        client.simulate_delete(f"{USR_URL}/{user_name}")
        response = client.simulate_get(USR_URL, headers=auth_headers)
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Deleted user is still authorized",
        )
