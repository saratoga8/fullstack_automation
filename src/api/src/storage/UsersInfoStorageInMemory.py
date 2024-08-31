from src.storage.UserInfoType import UserInfoType
from src.storage.UsersInfoStorage import UsersInfoStorage


class UsersInfoStorageInMemory(UsersInfoStorage):
    def __init__(self, user_info: UserInfoType | None = None):
        self._storage: dict[str, UserInfoType] = dict()
        if user_info is not None:
            self.add_info(user_info)

    def get_info(self, user_name: str) -> UserInfoType | None:
        if user_name:
            return self._storage.get(user_name, None)
        else:
            raise ValueError(f"Invalid user name '{user_name}'")

    def add_info(self, info: UserInfoType):
        user_name = info.name
        if not self._storage.get(user_name):
            self._storage[user_name] = info
        else:
            raise ValueError(f"User name '{user_name}' already exists")

    def delete(self, user_name: str):
        if user_name:
            if not self._storage.pop(user_name, None):
                raise ValueError(f"User '{user_name}' not found")
        else:
            raise ValueError(f"Invalid user name '{user_name}'")
