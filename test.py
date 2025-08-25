import asyncio
from googletrans import Translator


async def main():
    translator = Translator()
    translation = await translator.translate("Hello, world!", dest="ru")
    print(translation.text)  # ¡Hola Mundo!


asyncio.run(main())
