from json import loads

from hamcrest import assert_that, equal_to

from src.api.src.storage.UsersInfoStorageInMemory import UserInfoType
from src.api.tests.constants import USR_INFO_URL

METHOD_PATH = (
    "src.api.src.storage.UsersInfoStorageInMemory.UsersInfoStorageInMemory.get_info"
)


def test_get_info(mocker, client, user_info: UserInfoType):
    mock_get_info = mocker.patch(METHOD_PATH)
    mock_get_info.return_value = user_info

    response = client.simulate_get(f"{USR_INFO_URL}/{user_info.name}")

    assert_that(
        response.status_code,
        equal_to(200),
        "Invalid response status code",
    )
    assert_that(loads(response.text), equal_to(dict(user_info)), "Invalid user info")


def test_get_info_invalid_user(mocker, client):
    user_name = "bla"
    mock_get_info = mocker.patch(METHOD_PATH)
    mock_get_info.return_value = None

    response = client.simulate_get(f"{USR_INFO_URL}/{user_name}")

    assert_that(
        response.status_code,
        equal_to(404),
        "Invalid response status code",
    )
    assert_that(
        loads(response.text),
        equal_to({"error": f"User {user_name} not found"}),
        "Invalid error message",
    )
