from falcon import Response


def update_error_response(
    err: BaseException | str, err_code: int, resp: Response
) -> [str, int]:
    resp.text = str({"error": str(err)}).replace("'", '"')
    resp.status = err_code
