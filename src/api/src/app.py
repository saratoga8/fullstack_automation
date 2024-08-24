import falcon.asgi

from .UserInfo import UserInfo
from .UserOperations import UserOperations
from .storage.UsersInfoStorage import UsersInfoStorage


def create_app():
    app = falcon.asgi.App()

    storage = UsersInfoStorage()
    app.add_route("/user", UserOperations(storage))
    app.add_route("/user_info", UserInfo(storage))

    return app
