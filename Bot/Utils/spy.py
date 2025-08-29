import html
import logging
import asyncio
from typing import Optional, Callable, Awaitable

from aiogram import Bot
from aiogram.types import Message
from googletrans.client import TokenAcquirer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Bot.Database import MessageCache
from Bot.Utils.crypto import decrypt, encrypt


logger = logging.getLogger(__name__)


def escape_html(text: Optional[str]) -> str:
    """Экранирует текст для parse_mode=HTML"""
    return html.escape(text or "")


def build_caption(
    msg_type: str, chat_id: int, chat_title: str, caption: Optional[str]
) -> str:
    base = f"Отправитель: <a href='tg://user?id={chat_id}'><b>{escape_html(chat_title)}</b></a>\n"
    body = f"<blockquote><b>{escape_html(decrypt(token=caption))}</b></blockquote>"

    texts = {
        "Message": "🗑 Это сообщение было удалено:",
        "Photo": "🗑 Это фото было удалено:",
        "Video": "🗑 Это видео было удалено:",
        "Video_note": "🗑 Этот кружок был удалён:",
        "Voice": "🗑 Это голосовое было удалено:",
    }
    return f"{texts.get(msg_type, '🗑 Сообщение удалено:')}\n\n{base}Содержание: {body}"


async def send_deleted_message(
    bot: Bot, msg_type: str, target_id: int, file_id: Optional[str], caption_text: str
) -> None:
    handlers: dict[str, Callable[..., Awaitable[Message]]] = {
        "Message": bot.send_message,
        "Photo": bot.send_photo,
        "Video": bot.send_video,
        "Video_note": bot.send_video_note,
        "Voice": bot.send_voice,
    }

    if msg_type not in handlers:
        logger.warning(f"Unknown message type: {msg_type}")
        return

    kwargs = {"chat_id": target_id}

    if msg_type == "Message":
        kwargs.update(text=caption_text, parse_mode="HTML")
    else:
        media_arg = {
            "Photo": "photo",
            "Video": "video",
            "Video_note": "video_note",
            "Voice": "voice",
        }.get(msg_type)
        kwargs.update(
            {media_arg: file_id, "caption": caption_text, "parse_mode": "HTML"}
        )

    await handlers[msg_type](**kwargs)


async def DeleteHandler(message_id: int, bot: Bot, session: AsyncSession) -> None:
    try:
        request = select(MessageCache).where(MessageCache.Message_id == message_id)
        message = await session.scalar(request)

        if not message:
            return

        caption_text = build_caption(
            message.Type, message.Chat_id, message.Chat_full_name, message.Caption
        )

        # Удаляем из кэша
        await session.delete(message)
        await session.commit()

        # Куда слать? текстовые идут в user_id, остальные в chat_id
        target_id = message.User_id

        await send_deleted_message(
            bot, message.Type, target_id, message.File_id, caption_text
        )

    except Exception as ex:
        logger.exception(f"Ошибка в DeleteHandler: {ex}")


async def EditHandler(message: Message, session: AsyncSession) -> None:
    """Обработка редактирования бизнес-сообщений с кэшем"""
    try:
        bot = message.bot
        msg_id = int(f"{message.chat.id}{message.message_id}")
        connection = await bot.get_business_connection(message.business_connection_id)

        stmt = select(MessageCache).where(MessageCache.Message_id == msg_id)
        cached = await session.scalar(stmt)

        old_text = escape_html(cached.Caption if cached else None)
        new_text = escape_html(message.text)

        if cached:
            cached.Caption = encrypt(text=message.text or "")

            if message.from_user.id != cached.User_id:
                await bot.send_message(
                    cached.User_id,
                    f"🔏 Пользователь <a href='tg://user?id={message.from_user.id}'>{escape_html(message.from_user.full_name)}</a> "
                    f"изменил сообщение:\n\n"
                    f"Старый текст: <blockquote><b>{decrypt(token=old_text)}</b></blockquote>\n"
                    f"Новый текст: <blockquote><b>{new_text}</b></blockquote>",
                    parse_mode="HTML",
                )
        else:
            cached = MessageCache(
                Message_id=msg_id,
                Chat_id=message.chat.id,
                Chat_full_name=message.from_user.full_name,
                Caption=encrypt(text=message.text or ""),
                Type="Message",
                File_id="",  # если нет файла
                User_id=connection.user.id,
            )
            session.add(cached)

            if message.from_user.id != connection.user.id:
                await bot.send_message(
                    connection.user.id,
                    f"🔏 Пользователь <a href='tg://user?id={message.from_user.id}'>{escape_html(message.from_user.full_name)}</a> "
                    f"изменил сообщение, но старый текст отсутствует в кэше.\n\n"
                    f"Новый текст: <blockquote><b>{new_text}</b></blockquote>",
                    parse_mode="HTML",
                )

        await session.commit()
        await asyncio.sleep(0.05)

    except Exception as e:
        logger.error(f"Ошибка при обработке редактирования сообщения: {e}")
