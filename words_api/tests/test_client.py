import pytest

from words_api.client import (
    WordsAPIClientError,
    WordsAPIServerError,
    words_api_client,
)


class MockResponse:
    async def __aenter__(self, *args, **kwargs):
        return self

    async def __aexit__(self, *args, **kwargs):
        pass

    def __call__(self, url, headers):
        return self


class MockResponseOK(MockResponse):
    status = 200
    content = {"word": "Test", "synonyms": ["test1", "test2"]}

    async def json(self):
        return self.content


class MockResponseNotFound(MockResponse):
    status = 404


class MockResponseError(MockResponse):
    status = 500

    @property
    def text(self):
        return "Test error"


class MockResponseFailed(MockResponse):
    async def __aenter__(self, *args, **kwargs):
        raise Exception("Something went wrong")


class TestClient:
    @pytest.mark.asyncio
    async def test_ok(self, client, mocker):
        response = MockResponseOK()

        mocker.patch("words_api.client.words_api_client.session.get", response)

        description = await words_api_client.query_word("test")
        assert description == MockResponseOK.content

    @pytest.mark.asyncio
    async def test_not_found(self, client, mocker):
        response = MockResponseNotFound()

        mocker.patch("words_api.client.words_api_client.session.get", response)

        description = await words_api_client.query_word("test")
        assert description is None

    @pytest.mark.asyncio
    async def test_server_error(self, client, mocker):
        response = MockResponseError()

        mocker.patch("words_api.client.words_api_client.session.get", response)

        with pytest.raises(WordsAPIServerError):
            await words_api_client.query_word("test")

    @pytest.mark.asyncio
    async def test_client_error(self, client, mocker):
        response = MockResponseFailed()

        mocker.patch("words_api.client.words_api_client.session.get", response)

        with pytest.raises(WordsAPIClientError):
            await words_api_client.query_word("test")
