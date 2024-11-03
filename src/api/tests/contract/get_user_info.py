from http import HTTPStatus

import requests

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_INFO_URL


class TestGetUserInfo:
    _user_endpoint = f"{BASE_URL}/{USR_INFO_URL}"

    def test_get_user_info(self, user_info: UserInfoType):
        response = requests.get(f"{self._user_endpoint}/testuser")
        assert response.status_code == HTTPStatus.OK, "Invalid status code"
        response_data = dict(response.json())
        assert response_data.keys() == user_info.__dict__.keys(), "Invalid response data structure"
        for key, val in response_data.items():
            assert val, f"Invalid response data: '{key}' is empty"

    def test_user_not_found(self):
        response = requests.get(f"{self._user_endpoint}/notfound")
        assert response.status_code == HTTPStatus.NOT_FOUND, "Invalid status code"
        assert response.json() == {"error": "User not found"}, "Invalid response data"

    def test_server_error(self):
        response = requests.get(f"{self._user_endpoint}/testuser_500")
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, "Invalid status code"
        assert response.json() == {"error": "Internal Server Error"}, "Invalid response data"
