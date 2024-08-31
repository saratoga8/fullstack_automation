from falcon import Request, Response, HTTP_200, HTTP_500, HTTP_404

from src.utils.errors import update_error_response
from .storage import UsersInfoStorage


class UserInfo:
    def __init__(self, storage: UsersInfoStorage):
        self._storage: UsersInfoStorage = storage

    async def on_get(self, req: Request, resp: Response, name: str):
        try:
            if info := self._storage.get_info(name):
                resp.status = HTTP_200
                resp.text = str(info)
                resp.content_type = "application/json"
            else:
                update_error_response(f"User {name} not found", HTTP_404, resp)
        except ValueError as e:
            update_error_response(e, HTTP_500, resp)
