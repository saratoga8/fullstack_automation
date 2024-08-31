from hamcrest import assert_that, equal_to
from requests import codes

from src.storage.UserInfoType import UserInfoType
from tests.constants import USR_URL
from tests.utils.auth import create_auth_headers

METHOD_PATH = "src.storage.UsersInfoStorageInMemory.UsersInfoStorageInMemory.get_info"


def test_user_auth(mocker, client, user_info: UserInfoType):
    mock_get_info = mocker.patch(METHOD_PATH)
    mock_get_info.return_value = user_info

    response = client.simulate_get(USR_URL, headers=create_auth_headers(user_info))

    assert_that(response.status_code, equal_to(200), "User is not authorized")


def test_invalid_password_failed_auth(mocker, client, user_info: UserInfoType):
    headers = create_auth_headers(user_info)
    mock_get_info = mocker.patch(METHOD_PATH)
    user_info.password = "bla"
    mock_get_info.return_value = user_info

    response = client.simulate_get(USR_URL, headers=headers)

    assert_that(
        response.status_code,
        equal_to(codes.unauthorized),
        "Invalid status code",
    )


def test_invalid_user_failed_auth(mocker, client, user_info: UserInfoType):
    mock_get_info = mocker.patch(METHOD_PATH)
    mock_get_info.return_value = None

    response = client.simulate_get(USR_URL, headers=create_auth_headers(user_info))

    assert_that(
        response.status_code,
        equal_to(codes.not_found),
        "Invalid status code",
    )
