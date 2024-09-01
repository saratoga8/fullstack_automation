from hamcrest import assert_that, equal_to
from requests import request, codes

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_INFO_URL


def test_get_non_existing_user_info(user_info: UserInfoType):
    url = f"{BASE_URL}/{USR_INFO_URL}/{user_info.name}"

    response = request("GET", url)

    assert_that(
        response.status_code,
        equal_to(codes.not_found),
        "User should not be found",
    )
