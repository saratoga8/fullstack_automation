import base64
from json import loads

from falcon import (
    Request,
    Response,
    HTTP_200,
    HTTP_404,
    HTTP_500,
    HTTP_201,
    HTTP_409,
    HTTP_401,
)

from .storage.UsersInfoStorage import UsersInfoStorage


class UserOperations:
    def __init__(self, storage: UsersInfoStorage):
        self._storage = storage

    async def on_get(self, req: Request, resp: Response):
        creds = self._get_creds(req.auth)
        try:
            info = self._storage.get_info(creds["username"])
            if info:
                resp.status = (
                    HTTP_200 if info["password"] == creds["password"] else HTTP_401
                )
            else:
                resp.status = HTTP_404
        except ValueError as e:
            resp.data = b'{"error": e}'
            resp.status = HTTP_500

    @staticmethod
    def _get_creds(auth: str):
        encoded_part = auth.split(" ")[1]
        txt = base64.b64decode(encoded_part).decode("utf-8")
        creds = txt.split(":")
        return {"username": creds[0], "password": creds[1]}

    async def on_post(self, req: Request, resp: Response):
        user_info = loads(await req.stream.read())
        user_name = user_info["name"]
        try:
            if not self._storage.get_info(user_name):
                self._storage.add_info(user_info)
                resp.status = HTTP_201
            else:
                resp.status = HTTP_409
        except TypeError | ValueError as e:
            resp.data = b'{"error": e}'
            resp.status = HTTP_500

    async def on_delete(self, req: Request, resp: Response, name):
        try:
            self._storage.delete(name)
            resp.status = HTTP_200
        except ValueError as e:
            resp.data = b'{"error": e}'
            resp.status = HTTP_404
