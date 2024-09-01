from json import dumps

from hamcrest import assert_that, equal_to
from requests import request, codes

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_URL


def add_user(user_info: UserInfoType):
    url = f"{BASE_URL}/{USR_URL}"
    response = request("POST", url, data=dumps(dict(user_info)))

    assert_that(
        response.status_code,
        equal_to(codes.created),
        "Adding user: Invalid response status code",
    )
