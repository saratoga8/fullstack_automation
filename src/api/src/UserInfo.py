from falcon import Request, Response, HTTP_200, HTTP_500, HTTP_404

from .storage.UsersInfoStorage import UsersInfoStorage, UserInfoType


class UserInfo:
    def __init__(self, storage: UsersInfoStorage):
        self._storage = storage

    async def on_get(self, req: Request, resp: Response, name: str):
        try:
            info: UserInfoType | None = self._storage.get_info(name)
            if info:
                resp.status = HTTP_200
                resp.text = str(info).replace("'", '"')
                resp.content_type = "application/json"
            else:
                resp.status = HTTP_404
        except Exception as e:
            print(e)
            resp.data = b'{"error": e}'
            resp.status = HTTP_500
