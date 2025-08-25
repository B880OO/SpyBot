from aiogram import Router

from .handler import UserHandler
from .business import BusinessHandler
from .commands import CommandsHandler


def User_handler_router() -> Router:
    router = Router()

    UserHandler(router=router)
    CommandsHandler(router=router)
    BusinessHandler(router=router)

    return router
