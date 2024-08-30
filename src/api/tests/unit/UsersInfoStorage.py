import pytest
from hamcrest import assert_that, equal_to

from src.api.src.storage.UsersInfoStorageInMemory import (
    UsersInfoStorageInMemory,
    UserInfoType,
)


class TestUsersInfoStorage:
    def test_get_info(self, user_info: UserInfoType):
        storage = UsersInfoStorageInMemory(user_info)
        expected_user_info = storage.get_info(user_info.name)

        assert_that(expected_user_info, equal_to(user_info), "Invalid user info")

    def test_get_info_after_delete(self, user_info: UserInfoType):
        storage = UsersInfoStorageInMemory(user_info)
        user_name = user_info.name

        storage.delete(user_name)
        expected_user_info = storage.get_info(user_name)

        assert_that(expected_user_info, equal_to(None), "Invalid user info")

    def test_get_invalid_info(self):
        storage = UsersInfoStorageInMemory()
        try:
            storage.get_info("")
        except ValueError:
            return

        pytest.fail("Should return an error")

    def test_get_non_exist_info(self):
        storage = UsersInfoStorageInMemory()
        expected_user_info = storage.get_info("bla")

        assert_that(expected_user_info, equal_to(None), "Invalid user info")

    def test_add_info(self, user_info: UserInfoType):
        user_name = user_info.name

        storage = UsersInfoStorageInMemory()
        storage.add_info(user_info)
        actual_user_info = storage.get_info(user_name)

        assert_that(actual_user_info, equal_to(user_info), "Invalid added user info")

    def test_add_invalid_info(self, user_info: UserInfoType):
        user_info.last_name = ""

        try:
            UsersInfoStorageInMemory.add_info(user_info)
        except TypeError:
            return

        pytest.fail("Should return an error")

    def test_add_info_twice(self, user_info: UserInfoType):
        storage = UsersInfoStorageInMemory(user_info)

        try:
            storage.add_info(user_info)
        except ValueError:
            return

        pytest.fail("Should return an error")

    def test_delete(self, user_info: UserInfoType):
        storage = UsersInfoStorageInMemory(user_info)
        user_name = user_info.name

        storage.delete(user_name)

        assert_that(storage.get_info(user_name), equal_to(None), "User is not deleted")

    def test_delete_non_exist(self):
        try:
            UsersInfoStorageInMemory().delete("bla")
        except ValueError:
            return

        pytest.fail("Should return an error")

    def test_delete_twice(self, user_info: UserInfoType):
        storage = UsersInfoStorageInMemory(user_info)
        user_name = user_info.name

        try:
            storage.delete(user_name)
            storage.delete(user_name)
        except ValueError:
            return

        pytest.fail("Should return an error")

    def test_delete_invalid_name(self):
        try:
            UsersInfoStorageInMemory().delete("")
        except ValueError:
            return

        pytest.fail("Should return an error")
