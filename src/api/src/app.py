import falcon.asgi

from .UserInfo import UserInfo
from .UserOperations import UserOperations
from .storage.UsersInfoStorageInMemory import UsersInfoStorageInMemory


def create_app():
    app = falcon.asgi.App()

    storage = UsersInfoStorageInMemory()

    usr_ops = UserOperations(storage)
    usr_info = UserInfo(storage)

    app.add_route("/user", usr_ops)
    app.add_route("/user_info/{name}", usr_info)
    app.add_route("/user/{name}", usr_ops)

    return app
