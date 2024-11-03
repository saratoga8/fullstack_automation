import base64
import json
from typing import Optional

import falcon.asgi
from falcon import HTTP_200, HTTP_201, HTTP_400, HTTP_404, HTTP_409, Request, Response
from falcon.status_codes import HTTP_500
from pydantic import BaseModel, constr


class User(BaseModel):
    name: constr(min_length=1)
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ResponseError(BaseModel):
    error: str


existing_user_name = "testuser"
causing_500_user_name = "testuser_500"


def _update_err_response(error_message, status_code: Response.status, resp: Response):
    error = ResponseError(error=error_message)
    resp.status = status_code
    resp.text = error.json()


# Middleware for Basic Authentication (only for GET /user)
class BasicAuthMiddleware:
    async def process_request(self, req: Request, resp):
        # Enforce authentication only on GET /user endpoint
        if req.path == "/user" and req.method == "GET":
            auth_header = req.get_header("Authorization")
            if not auth_header:
                raise falcon.HTTPUnauthorized("Auth required", "Basic authentication is required")
            auth_type, credentials = auth_header.split(" ", 1)
            if auth_type.lower() != "basic":
                raise falcon.HTTPUnauthorized("Auth required", "Invalid auth type")

            try:
                username, password = base64.b64decode(credentials).decode().split(":")
                if username == causing_500_user_name:
                    raise falcon.HTTPInternalServerError
                if username != existing_user_name:
                    raise falcon.HTTPNotFound
                elif password != "password123":
                    raise falcon.HTTPUnauthorized
            except ValueError as e:
                raise falcon.HTTPBadRequest("bla", "opp")


class UserResource:
    async def on_get(self, req, resp):
        # This is the GET /user endpoint, requires BasicAuth
        resp.status = HTTP_200
        resp.text = json.dumps({"message": "User authenticated successfully"})

    async def on_post(self, req: Request, resp: Response):
        # This is the POST /user endpoint, does NOT require BasicAuth
        body = await req.media
        try:
            user = User(**body)
        except:
            _update_err_response("Invalid user data", HTTP_400, resp)
            return

        if user.name == existing_user_name:  # Mock condition for existing user
            _update_err_response("User already exists", HTTP_409, resp)
        elif user.name == causing_500_user_name:
            _update_err_response("Internal Server Error", HTTP_500, resp)
        else:
            resp.status = HTTP_201
            resp.text = json.dumps({"message": "User created successfully"})


class UserInfoResource:
    async def on_get(self, req, resp, name):
        if name == existing_user_name:  # Mock condition
            user = User(name=existing_user_name, password="password123", first_name="Test", last_name="User")
            resp.status = HTTP_200
            resp.text = user.json()
        elif name == causing_500_user_name:
            _update_err_response("Internal Server Error", HTTP_500, resp)
        else:
            _update_err_response("User not found", HTTP_404, resp)


class DeleteUserResource:
    async def on_delete(self, req, resp, name):
        if name == existing_user_name:  # Mock condition
            resp.status = HTTP_200
            resp.text = json.dumps({"message": "User deleted successfully"})
        else:
            _update_err_response("User not found", HTTP_404, resp)


class HealthCheckResource:
    async def on_get(self, req, resp):
        resp.status = HTTP_200
        resp.text = json.dumps({"status": "OK"})


# Initialize the Falcon app with ASGI compatibility and routes

app = falcon.asgi.App(middleware=[BasicAuthMiddleware()], cors_enable=True)

app.add_route("/user", UserResource())  # Handles both GET and POST /user
app.add_route("/user_info/{name}", UserInfoResource())
app.add_route("/user/{name}", DeleteUserResource())
app.add_route("/health", HealthCheckResource())

# To run the mock server with Uvicorn:
# 1. Save this file as falcon_asgi_server.py.
# 2. Run with: `uvicorn falcon_asgi_server:app --reload`
