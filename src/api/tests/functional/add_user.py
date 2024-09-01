from json import dumps

from hamcrest import assert_that, equal_to
from requests import request, codes

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_URL, USR_INFO_URL
from tests.functional.utils.user import add_user


class TestAddUser:

    def test_add_user(self, user_info: UserInfoType):
        add_user(user_info)

        url = f"{BASE_URL}/{USR_INFO_URL}/{user_info.name}"
        response = request("GET", url)

        assert_that(
            response.status_code,
            equal_to(codes.ok),
            "Getting user info: Invalid response status code",
        )

        assert_that(
            response.json(),
            equal_to(dict(user_info)),
            "Getting user info: Invalid response body",
        )

    def test_add_existing_user(self, user_info: UserInfoType):
        add_user(user_info)

        url = f"{BASE_URL}/{USR_URL}"
        response = request("POST", url, data=dumps(dict(user_info)))

        assert_that(
            response.status_code,
            equal_to(codes.conflict),
            "Invalid response status code",
        )
