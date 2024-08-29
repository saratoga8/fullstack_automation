from black.ranges import dataclass


@dataclass
class UserInfoType:
    name: str
    password: str
    first_name: str
    last_name: str

    def __init__(self, info: dict[str, str]):
        self.name = info.get("name", "")
        self.password = info.get("password", "")
        self.first_name = info.get("first_name", "")
        self.last_name = info.get("last_name", "")
        for key in self.__dict__.keys():
            if not self.__dict__[key]:
                raise ValueError(f"Invalid {key}")

    def __iter__(self):
        return iter(self.__dict__.items())

    def __str__(self):
        return str(self.__dict__).replace("'", '"')


class UsersInfoStorage:
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
