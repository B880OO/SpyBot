import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from Bot.Middleware import AdminMiddleware


class AdminHandler:
    def __init__(self, router: Router) -> None:
        self.router = router
        self._register_handlers()
        self.logger = logging.getLogger(__name__)
        self.router.message.middleware(AdminMiddleware())

    def _register_handlers(self) -> None:
        self.router.message(Command("admin"))(self.admin_cmd)

    async def admin_cmd(self, message: Message) -> None:
        await message.answer(text="Admin panel")
