import logging

from aiogram import Router, F
from aiogram.types import Message, BusinessConnection

from Bot.Utils.spy import EditHandler, DeleteHandler
from Bot.Utils.save import SaveHandler

from sqlalchemy.ext.asyncio import AsyncSession


class BusinessHandler:
    def __init__(self, router: Router) -> None:
        self.router = router
        self._register_handlers()
        self.logger = logging.getLogger(__name__)

    def _register_handlers(self) -> None:
        self.router.business_connection()(self.connection)
        self.router.business_message(F.text)(self.business_text)
        self.router.business_message(F.photo)(self.business_photo)
        self.router.business_message(F.video)(self.business_video)
        self.router.business_message(F.video_note)(self.business_video_note)
        self.router.business_message(F.voice)(self.business_voice)

        self.router.deleted_business_messages()(self.DeleteUpdate)
        self.router.edited_business_message()(self.EditUpdate)

    async def business_text(self, message: Message, session: AsyncSession) -> None:
        try:
            feedback = message.business_connection_id
            connection = await message.bot.get_business_connection(feedback)
            await SaveHandler(
                message=message,
                user_id=connection.user.id,
                message_type="Message",
                session=session,
            )
        except Exception as e:
            self.logger.error(msg=f"Error: {e}")

    async def business_photo(self, message: Message, session: AsyncSession) -> None:
        try:
            feedback = message.business_connection_id
            connection = await message.bot.get_business_connection(feedback)
            await SaveHandler(
                message=message,
                user_id=connection.user.id,
                message_type="Photo",
                session=session,
            )
        except Exception as e:
            self.logger.error(msg=f"Error: {e}")

    async def business_video(self, message: Message, session: AsyncSession) -> None:
        try:
            feedback = message.business_connection_id
            connection = await message.bot.get_business_connection(feedback)
            await SaveHandler(
                message=message,
                user_id=connection.user.id,
                message_type="Video",
                session=session,
            )
        except Exception as e:
            self.logger.error(msg=f"Error: {e}")

    async def business_video_note(
        self, message: Message, session: AsyncSession
    ) -> None:
        try:
            feedback = message.business_connection_id
            connection = await message.bot.get_business_connection(feedback)
            await SaveHandler(
                message=message,
                user_id=connection.user.id,
                message_type="Video_note",
                session=session,
            )
        except Exception as e:
            self.logger.error(msg=f"Error: {e}")

    async def business_voice(self, message: Message, session: AsyncSession) -> None:
        try:
            feedback = message.business_connection_id
            connection = await message.bot.get_business_connection(feedback)
            await SaveHandler(
                message=message,
                user_id=connection.user.id,
                message_type="Voice",
                session=session,
            )
        except Exception as e:
            self.logger.error(msg=f"Error: {e}")

    async def DeleteUpdate(self, message: Message, session: AsyncSession) -> None:
        try:
            bot = message.bot
            for ids in message.message_ids:
                message_id = int(f"{message.chat.id}{ids}")
            await DeleteHandler(message_id=message_id, bot=bot, session=session)
        except Exception as ex:
            self.logger.error(msg=f"Error: {ex}")

    async def EditUpdate(self, message: Message, session: AsyncSession) -> None:
        try:
            await EditHandler(message=message, session=session)
        except Exception as ex:
            self.logger.error(msg=f"Error: {ex}")

    async def connection(self, update: BusinessConnection) -> None:
        await update.bot.send_message(
            chat_id=update.user.id,
            text="Ты долбаеб, и подключил бота, теперь он у тебя спиздить звезды!!!",
        )
