import logging

import aiohttp
from fastapi import FastAPI

from config.settings import settings

logger = logging.getLogger(f"vocabulary_{__name__}")


class WordsAPIClientError(Exception):
    pass


class WordsAPIServerError(Exception):
    pass


class WordsAPIClient:
    session: aiohttp.ClientSession = None
    base_url = "https://wordsapiv1.p.rapidapi.com"
    headers = {
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "x-rapidapi-key": settings.WORDS_API_KEY,
    }

    def setup_session(self):
        self.session = aiohttp.ClientSession()

    async def close_session(self):
        if self.session:
            await self.session.close()
        self.session = None

    def init_app(self, app: FastAPI):
        @app.on_event("startup")
        def startup():
            self.setup_session()

        @app.on_event("shutdown")
        async def shutdown():
            await self.close_session()

    async def query_word(self, word: str):
        url = f"{self.base_url}/words/{word}"

        try:
            async with self.session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    json_result = await response.json()
                    return json_result
                elif response.status == 404:
                    return None
                logging.error(
                    response.text,
                    extra={"status": response.status, "word": word},
                )
                raise WordsAPIServerError(response.text)

        except WordsAPIServerError:
            raise
        except Exception as e:
            logging.error(
                e,
                extra={"url": url, "word": word},
            )
            raise WordsAPIClientError(e)


words_api_client = WordsAPIClient()
