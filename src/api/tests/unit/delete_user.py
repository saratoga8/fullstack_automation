from hamcrest import assert_that, equal_to
from requests import codes

from src.storage.UserInfoType import UserInfoType
from tests.constants import USR_URL

DELETE_METHOD_PATH = (
    "src.storage.UsersInfoStorageInMemory.UsersInfoStorageInMemory.delete"
)


def test_delete_user(mocker, client, user_info: UserInfoType):
    mock_del_info = mocker.patch(DELETE_METHOD_PATH)
    mock_del_info.return_value = None

    response = client.simulate_delete(f"/user/{user_info.name}")

    assert_that(
        response.status_code, equal_to(codes.ok), "Invalid response status code"
    )


def test_delete_invalid_user(mocker, client):
    mock_del_info = mocker.patch(
        DELETE_METHOD_PATH, side_effect=ValueError("Invalid user")
    )
    mock_del_info.return_value = None

    response = client.simulate_delete(f"{USR_URL}/bla")

    assert_that(
        response.status_code,
        equal_to(codes.not_found),
        "Invalid response status code",
    )
