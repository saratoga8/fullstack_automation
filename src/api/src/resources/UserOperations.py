import base64
import binascii
from dataclasses import dataclass
from json import loads, JSONDecodeError

from falcon import (
    Request,
    Response,
    HTTP_200,
    HTTP_404,
    HTTP_500,
    HTTP_201,
    HTTP_409,
    HTTP_401,
    HTTP_400,
)

from src.storage import UsersInfoStorage
from src.storage.UsersInfoStorageInMemory import UserInfoType
from src.utils.errors import update_error_response


@dataclass
class Credentials:
    username: str
    password: str

    def __init__(self, username: str, password: str):
        if not username:
            raise ValueError("Invalid username")
        if not password:
            raise ValueError("Invalid password")
        self.username = username
        self.password = password


class UserOperations:
    def __init__(self, storage: UsersInfoStorage):
        self._storage: UsersInfoStorage = storage

    async def on_get(self, req: Request, resp: Response):
        try:
            creds = self._get_creds(req.auth)
        except ValueError as e:
            update_error_response(e, HTTP_400, resp)
            return
        try:
            if info := self._storage.get_info(creds.username):
                resp.status = HTTP_200 if info.password == creds.password else HTTP_401
            else:
                resp.status = HTTP_404
        except ValueError as e:
            update_error_response(e, HTTP_500, resp)

    async def on_post(self, req: Request, resp: Response):
        try:
            user_info = UserInfoType(loads(await req.stream.read()))
            try:
                if not self._storage.get_info(user_info.name):
                    self._storage.add_info(user_info)
                    resp.status = HTTP_201
                else:
                    resp.status = HTTP_409
            except TypeError | ValueError as e:
                update_error_response(e, HTTP_500, resp)
        except (ValueError, TypeError, JSONDecodeError) as e:
            update_error_response(e, HTTP_400, resp)

    async def on_delete(self, _req: Request, resp: Response, name):
        try:
            self._storage.delete(name)
            resp.status = HTTP_200
        except ValueError as e:
            update_error_response(e, HTTP_404, resp)

    @staticmethod
    def _get_creds(auth: str) -> Credentials:
        if auth:
            if encoded_part := auth.split(" ")[1]:
                try:
                    txt = base64.b64decode(encoded_part).decode("utf-8")
                    creds = txt.split(":")
                    return Credentials(creds[0], creds[1])
                except (binascii.Error, UnicodeDecodeError) as e:
                    raise ValueError(f"Invalid auth header: {e}")
            else:
                raise ValueError("Invalid auth header: No encoded part")
        else:
            raise ValueError("Invalid auth header")
