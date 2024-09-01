from hamcrest import assert_that, equal_to
from requests import request, codes

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_URL, USR_INFO_URL
from tests.functional.utils.user import add_user
from tests.utils.auth import create_auth_headers


class TestE2E:
    def test_e2e(self, user_info: UserInfoType):
        add_user(user_info)

        url = f"{BASE_URL}/{USR_URL}"
        response = request("GET", url, headers=create_auth_headers(user_info))
        assert_that(response.status_code, equal_to(codes.ok), "User is not authorized")

        url = f"{BASE_URL}/{USR_INFO_URL}/{user_info.name}"
        response = request("GET", url)
        assert_that(
            response.json(),
            equal_to(dict(user_info)),
            "Invalid user info",
        )

        url = f"{BASE_URL}/{USR_URL}/{user_info.name}"
        request("DELETE", url)

        url = f"{BASE_URL}/{USR_INFO_URL}/{user_info.name}"
        response = request("GET", url)

        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "User should not be found",
        )
