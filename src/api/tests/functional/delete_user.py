from hamcrest import assert_that, equal_to
from requests import request, codes, Response

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_URL, USR_INFO_URL
from tests.functional.utils.user import add_user


class TestDeleteUser:

    @staticmethod
    def _deleting(user_name: str) -> Response:
        url = f"{BASE_URL}/{USR_URL}/{user_name}"
        return request("DELETE", url)

    def test_delete_user(self, user_info: UserInfoType):
        add_user(user_info)

        response = self._deleting(user_info.name)

        assert_that(
            response.status_code,
            equal_to(codes.ok),
            "Invalid response status code",
        )

        url = f"{BASE_URL}/{USR_INFO_URL}/{user_info.name}"
        response = request("GET", url)
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "User is not deleted",
        )

    def test_delete_nonexistent_user(self, user_info: UserInfoType):
        response = self._deleting(user_info.name)

        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "Invalid response status code",
        )

    def test_get_info_deleted_user(self, user_info: UserInfoType):
        add_user(user_info)

        self._deleting(user_info.name)

        url = f"{BASE_URL}/{USR_INFO_URL}/{user_info.name}"
        response = request("GET", url)
        assert_that(
            response.status_code,
            equal_to(codes.not_found),
            "User is not deleted",
        )
