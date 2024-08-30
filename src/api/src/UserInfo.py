from falcon import Request, Response, HTTP_200, HTTP_500, HTTP_404

from .storage import UsersInfoStorage
from ..tests.functional.utils.errors import update_error_response


class UserInfo:
    def __init__(self, storage: UsersInfoStorage):
        self._storage = storage

    async def on_get(self, req: Request, resp: Response, name: str):
        try:
            if info := self._storage.get_info(name):
                resp.status = HTTP_200
                resp.text = str(info)
                resp.content_type = "application/json"
            else:
                resp.status = HTTP_404
        except ValueError as e:
            update_error_response(e, HTTP_500, resp)
