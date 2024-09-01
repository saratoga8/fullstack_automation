from hamcrest import assert_that, equal_to
from requests import request, codes, Response

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_URL
from tests.functional.utils.user import add_user
from tests.utils.auth import create_auth_headers


class TestUserAuthorization:

    @staticmethod
    def _authorization(user_info: UserInfoType) -> Response:
        url = f"{BASE_URL}/{USR_URL}"
        return request("GET", url, headers=create_auth_headers(user_info))

    def test_user_authorization(self, user_info: UserInfoType):
        add_user(user_info)

        response = self._authorization(user_info)

        assert_that(
            response.status_code,
            equal_to(codes.ok),
            "Invalid status code",
        )

    def test_user_authorization_fail(self, user_info: UserInfoType):
        add_user(user_info)
        user_info.password = "bla"

        response = self._authorization(user_info)

        assert_that(
            response.status_code,
            equal_to(codes.unauthorized),
            "Invalid status code",
        )

    def test_non_existing_user_authorization_fail(self, user_info: UserInfoType):
        response = self._authorization(user_info)

        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Invalid status code",
        )
