import os
import asyncio
from aiogram.types import FSInputFile, Message


async def ttl_media(message: Message, file_type: str, send_method) -> bool:
    """Process and save media files from messages faster with temp/ storage."""
    try:
        media = getattr(message.reply_to_message, file_type, None)
        if not media:
            return False  # No media in reply

        # Get user_id and bot username from the message
        connection = await message.bot.get_business_connection(
            message.business_connection_id
        )
        user_id = connection.from_user.id
        bot_name = (await message.bot.get_me()).username

        # If multiple versions exist (e.g., photo sizes), pick the best quality
        media_file = media[-1] if isinstance(media, list) else media

        # Get file info
        file = await message.bot.get_file(media_file.file_id)
        check = file.file_id[:2]
        md = ["GA", "Fg", "Fw", "GQ"]

        if check in md:
            # Use temp/ directory for faster file handling
            os.makedirs("temp", exist_ok=True)
            local_file_path = os.path.join("temp", os.path.basename(file.file_path))

            # Download file directly to temp
            await message.bot.download_file(file.file_path, local_file_path)

            # Wrap file for re-upload
            media_input = FSInputFile(local_file_path)
            caption = f"<b>☝️Сохранено с помощью @{bot_name}</b>"

            # Send appropriate media type
            kwargs = {"caption": caption, "parse_mode": "HTML"}
            if file_type == "photo":
                await send_method(user_id, photo=media_input, **kwargs)
            elif file_type == "video":
                await send_method(user_id, video=media_input, **kwargs)
            elif file_type == "voice":
                await send_method(user_id, voice=media_input, **kwargs)
            elif file_type == "video_note":
                await send_method(user_id, video_note=media_input, **kwargs)

            # Clean up immediately
            try:
                os.remove(local_file_path)
            except OSError:
                pass

            await asyncio.sleep(0.01)
        return True

    except Exception as e:
        target_id = (
            connection.from_user.id
            if "connection" in locals()
            else message.from_user.id
        )
        await message.bot.send_message(
            target_id, f"Ошибка: Не удалось обработать {file_type}."
        )
        return False
