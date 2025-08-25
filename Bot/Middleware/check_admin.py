from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Awaitable, Callable, Dict, Any
from Bot.config import settings


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        if event.from_user.id in settings.ADMINS:
            return await handler(event, data)
        else:
            return
