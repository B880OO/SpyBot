import aiohttp
import asyncio

from Bot.config import settings


async def ask(request: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.AI_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "google/gemma-3-27b-it:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": request,
                    },
                ],
            }
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            data = await resp.json()
            return data


async def main():
    result = await ask(
        request="Can u code me telegram bot in js which send me echo messages use only js without libs"
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
