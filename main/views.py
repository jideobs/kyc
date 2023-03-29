from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import HTTPResponse


class VerifyBankAccountView(HTTPMethodView):
    def __init__(self) -> None:
        pass

    async def post(self, request: Request) -> HTTPResponse:
        pass


class VerifyBvnView(HTTPMethodView):
    def __init__(self) -> None:
        pass

    async def post(self, request: Request) -> HTTPResponse:
        pass


class VerifyWalletAccountView(HTTPMethodView):
    def __init__(self) -> None:
        pass

    async def post(self, request: Request) -> HTTPResponse:
        pass
