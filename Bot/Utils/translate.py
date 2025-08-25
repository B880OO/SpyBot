from Bot.config import translator


async def tr(text: str) -> str:
    translation = await translator.translate(text, dest="ru")
    return translation.text
