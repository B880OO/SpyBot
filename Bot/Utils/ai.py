import aiohttp
import asyncio

API_KEY = "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"


async def ask_image():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "google/gemma-3-27b-it:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is in this image?"},
                ],
            }
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            data = await resp.json()
            return data


async def main():
    result = await ask_image()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
