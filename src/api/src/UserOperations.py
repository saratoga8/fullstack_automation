from falcon import Request, Response, HTTP_200, HTTP_500, HTTP_201, HTTP_401, HTTP_404

from .storage.UsersInfoStorage import UsersInfoStorage


class UserOperations:
    _user_name_txt = "user_name"
    _password_txt = "password"

    def __init__(self, storage: UsersInfoStorage):
        self._storage = storage

    async def on_get(self, req: Request, resp: Response):
        creds = req.auth
        print(creds)
        try:
            info = self._storage.get_info(creds["username"])
            if info:
                resp.status = (
                    HTTP_200 if info["password"] == creds["password"] else HTTP_401
                )
            else:
                resp.status = HTTP_404
        except ValueError as e:
            resp.data = {"error": e}
            resp.status = HTTP_500

    async def on_post(self, req: Request, resp: Response):
        user_info = await req.stream.read()
        try:
            self._storage.add_info(user_info)
            resp.status = HTTP_201
        except TypeError | ValueError as e:
            resp.data = {"error": e}
            resp.status = HTTP_500

    async def on_delete(self, req: Request, resp: Response):
        user_name = req.path.split("/")[-1]
        try:
            self._storage.delete(user_name)
            resp.status = HTTP_200
        except ValueError as e:
            resp.data = {"error": e}
            resp.status = HTTP_500

    def _params_valid(self, req: Request) -> bool:
        params = req.params
        if params:
            if not params.get(self._user_name_txt):
                print(f"Missing {self._user_name_txt} in the request {req.path}")
                return False
            if not params.get(self._password_txt):
                print(f"Missing {self._password_txt} in the request {req.path}")
                return False
        else:
            print(f"There are no parameters in the request {req.path}")
            return False

        return True
