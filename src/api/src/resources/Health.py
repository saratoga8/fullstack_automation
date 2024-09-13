from falcon import Request, Response, HTTP_200


class Health:

    @staticmethod
    async def on_get(_req: Request, resp: Response):
        resp.status = HTTP_200
