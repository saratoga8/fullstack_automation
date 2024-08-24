from falcon import Request, Response, HTTP_200, HTTP_500, HTTP_404

from .storage.UsersInfoStorage import UsersInfoStorage


class UserInfo:
    def __init__(self, storage: UsersInfoStorage):
        self._storage = storage

    async def on_get(self, req: Request, resp: Response):
        user_name = req.params.get("username")
        try:
            if info := self._storage.get_info(user_name):
                resp.status = HTTP_200
                resp.data = info
            else:
                resp.status = HTTP_404
        except ValueError as e:
            resp.data = {"error": e}
            resp.status = HTTP_500
