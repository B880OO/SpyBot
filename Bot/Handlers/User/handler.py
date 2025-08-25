import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Bot.Database import User


class UserHandler:
    def __init__(self, router: Router) -> None:
        self.router = router
        self._register_handlers()
        self.logger = logging.getLogger(__name__)

    def _register_handlers(self) -> None:
        self.router.message(Command("start"))(self.start_cmd)
        self.router.message(F.text)(self.echo_message)

    async def start_cmd(self, message: Message, session: AsyncSession) -> None:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username

        user = await session.scalar(select(User).where(User.Telegram_id == user_id))
        if user is None:
            new_user = User(
                Telegram_id=user_id, First_name=first_name, Username=username
            )
            session.add(new_user)
        await message.answer(
            text="Well come to bot for spy bot, for save deleted messages!!!"
        )

    async def echo_message(self, message: Message) -> None:
        await message.answer(
            text=f"User ID: {message.from_user.id}\nSend message: {message.text}"
        )
