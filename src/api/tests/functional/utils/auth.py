import base64

from src.api.src.storage.UsersInfoStorage import UserInfoType


def create_auth_headers(user_info: UserInfoType) -> dict[str, str]:
    creds_txt = f"{user_info.name}:{user_info.password}"
    creds_encoded = base64.b64encode(creds_txt.encode("utf-8")).decode("utf-8")

    return {"Authorization": f"Basic {creds_encoded}"}
