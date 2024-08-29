from json import dumps, loads

from falcon.testing import TestClient
from hamcrest import assert_that, equal_to
from requests import codes

from src.api.src.storage.UsersInfoStorage import UserInfoType
from src.api.tests.constants import USR_URL


class TestRouteParameters:
    def test_add_user_params(self, user_info: UserInfoType, client: TestClient):
        invalid_info = dict(user_info).copy()
        key = list(invalid_info.keys())[0]
        invalid_info.pop(key)

        response = client.simulate_post(USR_URL, body=dumps(invalid_info))

        assert_that(
            response.status_code,
            equal_to(codes.bad_request),
            "Invalid response status code",
        )
        assert_that(
            loads(response.text)["error"],
            equal_to(f"Invalid {key}"),
            "Invalid error message in response",
        )
