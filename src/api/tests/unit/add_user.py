from json import dumps, loads

from hamcrest import assert_that, equal_to
from requests import codes

from src.storage.UserInfoType import UserInfoType
from tests.constants import USR_URL

ADD_INFO_METHOD_PATH = (
    "src.storage.UsersInfoStorageInMemory.UsersInfoStorageInMemory.add_info"
)
GET_INFO_METHOD_PATH = (
    "src.storage.UsersInfoStorageInMemory.UsersInfoStorageInMemory.get_info"
)


def test_add_user(mocker, client, user_info: UserInfoType):
    mock_add_info = mocker.patch(ADD_INFO_METHOD_PATH)
    mock_add_info.return_value = None
    response = client.simulate_post(USR_URL, body=dumps(dict(user_info)))

    assert_that(
        response.status_code,
        equal_to(codes.created),
        "Invalid response status code",
    )


def test_try_add_existing_user(mocker, client, user_info: UserInfoType):
    mock_add_info = mocker.patch(ADD_INFO_METHOD_PATH)
    mock_add_info.return_value = None
    mock_add_info = mocker.patch(GET_INFO_METHOD_PATH)
    mock_add_info.return_value = user_info

    response = client.simulate_post(USR_URL, body=dumps(dict(user_info)))

    assert_that(
        response.status_code,
        equal_to(codes.conflict),
        "Invalid response status code",
    )


def test_add_user_invalid_info(user_info: UserInfoType, client):
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
