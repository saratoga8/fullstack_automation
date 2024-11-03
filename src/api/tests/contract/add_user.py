import json
from http import HTTPStatus

import requests

from src.storage.UserInfoType import UserInfoType
from tests.constants import BASE_URL, USR_URL


class TestUserCreation:
    _user_endpoint = f"{BASE_URL}/{USR_URL}"

    @staticmethod
    def _post_request(user_info: UserInfoType) -> requests.Response:
        return requests.post(TestUserCreation._user_endpoint, data=json.dumps(dict(user_info)))

    def test_valid_user_creation(self, user_info: UserInfoType):
        response = self._post_request(user_info)

        assert response.status_code == HTTPStatus.CREATED, "Invalid status code"

    def test_existing_user(self, user_info: UserInfoType):
        user_info.name = "testuser"
        response = self._post_request(user_info)

        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json() == {"error": "User already exists"}

    def test_invalid_user_data(self, user_info: UserInfoType):
        user_info.name = ""
        response = self._post_request(user_info)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"error": "Invalid user data"}

    def test_server_error(self, user_info: UserInfoType):
        user_info.name = "testuser_500"
        response = self._post_request(user_info)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Internal Server Error"}
