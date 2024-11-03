from http import HTTPStatus

import requests

from tests.constants import BASE_URL, USR_URL


class TestUserDelete:
    _user_endpoint = f"{BASE_URL}/{USR_URL}"

    def test_delete_user(self):
        response = requests.delete(f"{self._user_endpoint}/testuser")

        assert response.status_code == HTTPStatus.OK, "Invalid status code"

    def test_delete_nonexistent_user(self):
        response = requests.delete(f"{self._user_endpoint}/nonexistentuser")

        assert response.status_code == HTTPStatus.NOT_FOUND, "Invalid status code"
