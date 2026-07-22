import os

from dotenv import load_dotenv
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

load_dotenv()


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()

        username = form.get("username")
        password = form.get("password")

        if (
            username == os.getenv("ADMIN_USERNAME")
            and password == os.getenv("ADMIN_PASSWORD")
        ):
            request.session.update({
                "admin_authenticated": True
            })
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get(
            "admin_authenticated",
            False
        )