import logging
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from Bot.Database import MessageCache

logger = logging.getLogger(__name__)


async def SaveHandler(
    message: Message, user_id: int, message_type: str, session: AsyncSession
):
    try:
        message_id = int(f"{message.chat.id}:{message.message_id}")

        caption = message.caption or message.text or ""
        file_id = None

        if message_type == "Message":
            caption = message.text or ""
        elif message_type == "Photo" and message.photo:
            file_id = message.photo[-1].file_id
        elif message_type == "Video" and message.video:
            file_id = message.video.file_id
        elif message_type == "Video_note" and message.video_note:
            file_id = message.video_note.file_id
        elif message_type == "Voice" and message.voice:
            file_id = message.voice.file_id

        saved_message = MessageCache(
            Message_id=message_id,
            Chat_id=message.chat.id,
            Chat_full_name=message.from_user.full_name,
            User_id=user_id,
            Type=message_type,
            Caption=caption,
            File_id=file_id,
        )

        session.add(saved_message)
    except Exception as ex:
        logger.error(f"Save Error: {ex}")
