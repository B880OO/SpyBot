import time
import random
import logging
import asyncio

from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    FSInputFile,
    InputProfilePhotoStatic,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from Bot.config import trole
from Bot.Utils.formater import en_ru


class CommandsHandler:
    def __init__(self, router: Router) -> None:
        self.router = router
        self._register_handlers()
        self.logger = logging.getLogger(__name__)

    def _register_handlers(self) -> None:
        self.router.business_message(F.text == ".help")(self.help_command)
        self.router.business_message(F.text == ".trole")(self.trole_command)
        self.router.business_message(F.text == ".love")(self.love_command)
        self.router.business_message(F.text == ".1000-7")(self.ghole_command)
        self.router.business_message(F.text == ".format")(self.format_command)

        self.router.business_message(F.text.startswith(".typing"))(self.typing_command)
        self.router.business_message(F.text.startswith(".node"))(self.node_command)
        self.router.business_message(F.text.startswith(".voice"))(self.voice_command)

    async def _send_message(
        self,
        bot: Bot,
        chat_id: int,
        business_connection_id: str,
        action: str,
        delay: int,
    ) -> None:
        start = time.time()
        while time.time() - start < delay:
            await bot.send_chat_action(
                chat_id=chat_id,
                business_connection_id=business_connection_id,
                action=action,
            )
            await asyncio.sleep(3)

    async def help_command(self, message: Message) -> None:
        me = await message.bot.get_me()

        caption = (
            "<b><tg-emoji emoji-id='5257965174979042426'>📝</tg-emoji> Commands:</b>\n"
            "<blockquote>"
            " <code>.trole</code> — <b>Отправляет шаблон для тролинга</b>\n"
            " <code>.love</code> — <b>Магическая анимация любви</b>\n"
            " <code>.1000-7</code> — <b>Отправляет пасту анимешникам, и меняет аву</b>\n"
            " <code>.format</code> — <b>Если перепутали раскладку текста</b>\n"
            "</blockquote>\n"
            "<blockquote>"
            " <code>.typing (delay)</code> — <b>Фейк печатание в чате</b>\n"
            " <code>.node (delay)</code> — <b>Фейк запись видео кружков</b>\n"
            " <code>.voice (delay)</code> — <b>Фейк запись голосового</b>\n"
            "</blockquote>"
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Перейти в бота", url=f"https://t.me/{me.username}"
                    )
                ]
            ]
        )

        await message.edit_text(text=caption, parse_mode="HTML", reply_markup=keyboard)

    async def trole_command(self, message: Message) -> None:
        feedback = message.business_connection_id
        business_connection = await message.bot.get_business_connection(feedback)
        if message.from_user.id == business_connection.user.id:
            try:
                await message.bot.delete_business_messages(
                    business_connection_id=feedback, message_ids=[message.message_id]
                )
                for text in trole:
                    await message.answer(text=text)
                    await asyncio.sleep(0.15)
            except Exception as e:
                self.logger.warning(msg=f"Error: {e}")

    async def love_command(self, message: Message) -> None:
        feedback = message.business_connection_id
        business_connection = await message.bot.get_business_connection(feedback)
        if message.from_user.id == business_connection.user.id:
            try:
                arr = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "💖"]
                h = "🤍"
                first = ""
                for i in "".join(
                    [
                        h * 9,
                        "\n",
                        h * 2,
                        arr[0] * 2,
                        h,
                        arr[0] * 2,
                        h * 2,
                        "\n",
                        h,
                        arr[0] * 7,
                        h,
                        "\n",
                        h,
                        arr[0] * 7,
                        h,
                        "\n",
                        h,
                        arr[0] * 7,
                        h,
                        "\n",
                        h * 2,
                        arr[0] * 5,
                        h * 2,
                        "\n",
                        h * 3,
                        arr[0] * 3,
                        h * 3,
                        "\n",
                        h * 4,
                        arr[0],
                        h * 4,
                    ]
                ).split("\n"):
                    first += i + "\n"
                    await message.edit_text(first)
                    await asyncio.sleep(0.3)
                for i in arr:
                    await message.edit_text(
                        "".join(
                            [
                                h * 9,
                                "\n",
                                h * 2,
                                i * 2,
                                h,
                                i * 2,
                                h * 2,
                                "\n",
                                h,
                                i * 7,
                                h,
                                "\n",
                                h,
                                i * 7,
                                h,
                                "\n",
                                h,
                                i * 7,
                                h,
                                "\n",
                                h * 2,
                                i * 5,
                                h * 2,
                                "\n",
                                h * 3,
                                i * 3,
                                h * 3,
                                "\n",
                                h * 4,
                                i,
                                h * 4,
                                "\n",
                                h * 9,
                            ]
                        )
                    )
                    await asyncio.sleep(0.35)
                for _ in range(8):
                    rand = random.choices(arr, k=34)
                    await message.edit_text(
                        "".join(
                            [
                                h * 9,
                                "\n",
                                h * 2,
                                rand[0],
                                rand[1],
                                h,
                                rand[2],
                                rand[3],
                                h * 2,
                                "\n",
                                h,
                                rand[4],
                                rand[5],
                                rand[6],
                                rand[7],
                                rand[8],
                                rand[9],
                                rand[10],
                                h,
                                "\n",
                                h,
                                rand[11],
                                rand[12],
                                rand[13],
                                rand[14],
                                rand[15],
                                rand[16],
                                rand[17],
                                h,
                                "\n",
                                h,
                                rand[18],
                                rand[19],
                                rand[20],
                                rand[21],
                                rand[22],
                                rand[23],
                                rand[24],
                                h,
                                "\n",
                                h * 2,
                                rand[25],
                                rand[26],
                                rand[27],
                                rand[28],
                                rand[29],
                                h * 2,
                                "\n",
                                h * 3,
                                rand[30],
                                rand[31],
                                rand[32],
                                h * 3,
                                "\n",
                                h * 4,
                                rand[33],
                                h * 4,
                                "\n",
                                h * 9,
                            ]
                        )
                    )
                    await asyncio.sleep(0.35)
                fourth = "".join(
                    [
                        h * 9,
                        "\n",
                        h * 2,
                        arr[0] * 2,
                        h,
                        arr[0] * 2,
                        h * 2,
                        "\n",
                        h,
                        arr[0] * 7,
                        h,
                        "\n",
                        h,
                        arr[0] * 7,
                        h,
                        "\n",
                        h,
                        arr[0] * 7,
                        h,
                        "\n",
                        h * 2,
                        arr[0] * 5,
                        h * 2,
                        "\n",
                        h * 3,
                        arr[0] * 3,
                        h * 3,
                        "\n",
                        h * 4,
                        arr[0],
                        h * 4,
                        "\n",
                        h * 9,
                    ]
                )
                await message.edit_text(fourth)
                for _ in range(47):
                    fourth = fourth.replace("🤍", "❤️", 1)
                    await message.edit_text(fourth)
                    await asyncio.sleep(0.25)
                for i in range(8):
                    await message.edit_text((arr[0] * (8 - i) + "\n") * (8 - i))
                    await asyncio.sleep(0.4)
                for i in ["I", "I ❤️", "I ❤️ YOU"]:
                    await message.edit_text(f"<b>{i}</b>", parse_mode="HTML")
                    await asyncio.sleep(0.5)
            except Exception as e:
                self.logger.warning(msg=f"Error: {e}")

    async def ghole_command(self, message: Message) -> None:
        feedback = message.business_connection_id
        business_connection = await message.bot.get_business_connection(feedback)
        if message.from_user.id == business_connection.user.id:
            try:
                await message.edit_text(
                    text="<b>Аниме на аве, мать в канаве</b>", parse_mode="HTML"
                )
                registration_image_path = "Photo/logo.jpg"
                registration_photo = FSInputFile(registration_image_path)
                await message.bot.set_business_account_profile_photo(
                    business_connection_id=message.business_connection_id,
                    photo=InputProfilePhotoStatic(photo=registration_photo),
                )
            except Exception as e:
                self.logger.warning(msg=f"Error: {e}")

    async def format_command(self, message: Message) -> None:
        feedback = message.business_connection_id
        business_connection = await message.bot.get_business_connection(feedback)

        if message.from_user.id == business_connection.user.id:
            try:
                if message.reply_to_message:
                    edition_id = message.reply_to_message.message_id
                    edition_text = message.reply_to_message.text or ""

                    converted = "".join(en_ru.get(ch, ch) for ch in edition_text)

                    if converted != edition_text:
                        await message.bot.edit_business_message_text(
                            business_connection_id=feedback,
                            message_id=edition_id,
                            text=converted,
                        )
                    await message.bot.delete_business_messages(
                        business_connection_id=feedback,
                        message_ids=[message.message_id],
                    )
                else:
                    await message.edit_text(text="Ответом на сообщение!!")
            except Exception as ex:
                self.logger.warning(msg=f"Error: {ex}")

    async def typing_command(self, message: Message) -> None:
        feedback = message.business_connection_id
        business_connection = await message.bot.get_business_connection(feedback)

        if message.from_user.id == business_connection.user.id:
            try:
                data = message.text[len(".typing ") :].strip()

                delay = 30

                if data.isdigit():
                    delay = int(data)

                await message.bot.delete_business_messages(
                    business_connection_id=feedback, message_ids=[message.message_id]
                )

                await self._send_message(
                    bot=message.bot,
                    chat_id=message.chat.id,
                    business_connection_id=feedback,
                    action="typing",
                    delay=delay,
                )
            except Exception as ex:
                self.logger.warning(msg=f"Error: {ex}")

    async def node_command(self, message: Message) -> None:
        feedback = message.business_connection_id
        business_connection = await message.bot.get_business_connection(feedback)

        if message.from_user.id == business_connection.user.id:
            try:
                data = message.text[len(".node ") :].strip()

                delay = 30

                if data.isdigit():
                    delay = int(data)

                await message.bot.delete_business_messages(
                    business_connection_id=feedback, message_ids=[message.message_id]
                )

                await self._send_message(
                    bot=message.bot,
                    chat_id=message.chat.id,
                    business_connection_id=feedback,
                    action="record_video_note",
                    delay=delay,
                )
            except Exception as ex:
                self.logger.warning(msg=f"Error: {ex}")

    async def voice_command(self, message: Message) -> None:
        feedback = message.business_connection_id
        business_connection = await message.bot.get_business_connection(feedback)

        if message.from_user.id == business_connection.user.id:
            try:
                data = message.text[len(".voice ") :].strip()

                delay = 30

                if data.isdigit():
                    delay = int(data)

                await message.bot.delete_business_messages(
                    business_connection_id=feedback, message_ids=[message.message_id]
                )

                await self._send_message(
                    bot=message.bot,
                    chat_id=message.chat.id,
                    business_connection_id=feedback,
                    action="record_voice",
                    delay=delay,
                )
            except Exception as ex:
                self.logger.warning(msg=f"Error: {ex}")
