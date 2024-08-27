type UserInfoType = {"name": str, "password": str, "first_name": str, "last_name": str}


class UsersInfoStorage:
    def __init__(self):
        self._storage: dict[str, UserInfoType] = {}

    def get_info(self, user_name: str) -> UserInfoType | None:
        if user_name:
            return self._storage.get(user_name, None)
        else:
            raise ValueError(f"Invalid user name '{user_name}'")

    def add_info(self, info: UserInfoType):
        user_name = info["name"]
        if not self._storage.get(user_name):
            err = self._check_info(info)
            if not err:
                self._storage[user_name] = info
            else:
                raise ValueError(f"Invalid user info: {err}")
        else:
            raise ValueError(f"User name '{user_name}' already exists")

    @staticmethod
    def _check_info(info: UserInfoType) -> str:
        for key in dict(info).keys():
            if not info[key]:
                return f"Invalid value of {key}"
        return ""

    def delete(self, user_name: str):
        if user_name:
            if not self._storage.pop(user_name, None):
                raise ValueError(f"User '{user_name}' not found")
        else:
            raise ValueError(f"Invalid user name '{user_name}'")
