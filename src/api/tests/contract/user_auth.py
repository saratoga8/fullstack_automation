from hamcrest import assert_that, equal_to
from requests import request, codes, Response

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_URL
from tests.utils.auth import create_auth_headers, create_invalid_auth_headers


class TestAuthentication:
    @staticmethod
    def _request_with_auth(user_info: UserInfoType) -> Response:
        url = f"{BASE_URL}/{USR_URL}"
        return request("GET", url, headers=create_auth_headers(user_info))

    @staticmethod
    def _request_with_invalid_auth() -> Response:
        url = f"{BASE_URL}/{USR_URL}"
        return request("GET", url, headers=create_invalid_auth_headers())

    def test_valid_creds(self, user_info: UserInfoType):
        user_info.name = "testuser"
        user_info.password = "password123"
        response = self._request_with_auth(user_info)

        assert_that(response.status_code, equal_to(codes.ok), "Invalid status code")

    def test_invalid_creds(self):
        response = self._request_with_invalid_auth()

        assert_that(response.status_code, equal_to(codes.bad_request), "Invalid status code")

    def test_invalid_password(self, user_info: UserInfoType):
        user_info.name = "testuser"
        response = self._request_with_auth(user_info)

        assert_that(response.status_code, equal_to(codes.unauthorized), "Invalid status code")

    def test_invalid_username(self, user_info: UserInfoType):
        response = self._request_with_auth(user_info)

        assert_that(response.status_code, equal_to(codes.not_found), "Invalid status code")

    def test_internal_server_error(self, user_info: UserInfoType):
        user_info.name = "testuser_500"
        response = self._request_with_auth(user_info)

        assert_that(response.status_code, equal_to(codes.internal_server_error), "Invalid status code")
