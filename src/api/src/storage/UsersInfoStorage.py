from abc import abstractmethod
from typing import Protocol

from src.storage.UserInfoType import UserInfoType


class UsersInfoStorage(Protocol):
    @abstractmethod
    def get_info(self, user_name: str) -> UserInfoType | None: ...

    @abstractmethod
    def add_info(self, info: UserInfoType) -> None: ...

    @abstractmethod
    def delete(self, user_name: str) -> None: ...
