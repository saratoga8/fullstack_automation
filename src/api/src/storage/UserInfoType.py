from dataclasses import dataclass


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
