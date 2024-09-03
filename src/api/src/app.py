import falcon.asgi

from src.resources.UserInfo import UserInfo
from src.resources.UserOperations import UserOperations
from .resources.Health import Health
from .storage.UsersInfoStorage import UsersInfoStorage
from .storage.UsersInfoStorageInMemory import UsersInfoStorageInMemory


def create_app(storage: UsersInfoStorage = UsersInfoStorageInMemory()):
    app = falcon.asgi.App(cors_enable=True)

    usr_ops = UserOperations(storage)
    usr_info = UserInfo(storage)

    app.add_route("/user", usr_ops)
    app.add_route("/user_info/{name}", usr_info)
    app.add_route("/user/{name}", usr_ops)
    app.add_route("/health", Health())

    return app
