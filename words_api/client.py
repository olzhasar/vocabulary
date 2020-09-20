import asyncio

import aiohttp
from fastapi import HTTPException

from settings import settings


class WordsAPIClient:
    sem: asyncio.Semaphore = None
    session: aiohttp.ClientSession = None
    base_url = "https://wordsapiv1.p.rapidapi.com"
    headers = {
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "x-rapidapi-key": settings.WORDS_API_KEY,
    }

    @classmethod
    def get_session(cls) -> aiohttp.ClientSession:
        if cls.session is None:
            cls.session = aiohttp.ClientSession()
        return cls.session

    @classmethod
    async def close_session(cls):
        if cls.session:
            await cls.session.close()
            cls.session = None

    @classmethod
    async def query_word(cls, word: str):
        session = cls.get_session()
        url = f"{cls.base_url}/words/{word}"

        try:
            async with session.get(url, headers=cls.headers) as response:
                if response.status != 200:
                    raise HTTPException(404, "Word not found")

                json_result = await response.json()
        except Exception as e:
            return {"ERROR": e}

        return json_result
