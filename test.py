# import asyncio
# from googletrans import Translator


# async def main():
#    translator = Translator()
#    translation = await translator.translate("Hello, world!", dest="ru")
#    print(translation.text)  # ¡Hola Mundo!


# asyncio.run(main())


import asyncio
from Bot.Utils.ai import ask


async def main():
    response = await ask(
        "Can you make me a echo telegram bot, with js and, don't use libs"
    )
    res = response.get("message")
    print(response["choices"][0]["message"]["content"])


asyncio.run(main=main())
