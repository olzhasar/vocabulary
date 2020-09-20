import pytest

from api.auth import generate_access_token
from db.models import User, UserWord, Word
from db.tests.factories import UserFactory, WordFactory


@pytest.mark.asyncio
async def test_login(client, use_db):
    await UserFactory(email="vincent@vega.com", password="pulpfiction")

    response = await client.post(
        "/token", data=dict(username="vincent@vega.com", password="pulpfiction")
    )

    assert response.status_code == 200

    response_json = response.json()
    assert "access_token" in response_json
    assert "token_type" in response_json


@pytest.mark.asyncio
async def test_bad_login(client, use_db):
    await UserFactory(email="vincent@vega.com", password="pulpfiction")

    response = await client.post(
        "/token",
        data=dict(username="vincent@vega.com", password="wrongpassword"),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup(client, use_db):
    response = await client.post(
        "/signup",
        json=dict(
            email="vincent@vega.com",
            password="pulpfiction",
            repeat_password="pulpfiction",
        ),
    )

    assert response.status_code == 201

    user_from_db = await User.query.where(
        User.email == "vincent@vega.com"
    ).gino.first()

    assert user_from_db
    assert user_from_db.check_password("pulpfiction")


@pytest.mark.asyncio
async def test_signup_email_in_use(client, use_db):
    await UserFactory(email="vincent@vega.com")

    response = await client.post(
        "/signup",
        json=dict(
            email="vincent@vega.com",
            password="pulpfiction",
            repeat_password="pulpfiction",
        ),
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_word_list_unauthenticated(client, use_db):
    response = await client.get("/words")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_word_list_ok(client, use_db):
    user = await UserFactory(email="vincent@vega.com")
    token = generate_access_token(user.email)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/words", headers=headers)
    assert response.status_code == 200


class TestWordAdd:
    @pytest.fixture
    def mock_words_api_query_word(self, monkeypatch):
        async def _query_word(word: str):
            return "Test"

        monkeypatch.setattr("api.views.WordsAPIClient.query_word", _query_word)

    @pytest.fixture
    @pytest.mark.asyncio
    async def data(self, use_db):
        user = await UserFactory(email="vincent@vega.com")

        for _word in ["banana", "apple", "fruit"]:
            word = await Word.create(name=_word)
            await UserWord.create(user_id=user.id, word_id=word.id)

        token = generate_access_token(user.email)
        headers = {"Authorization": f"Bearer {token}"}

        return {"user": user, "token": token, "headers": headers}

    @pytest.mark.asyncio
    async def test_add_new_word(self, client, data, mock_words_api_query_word):
        response = await client.post("/words/orange", headers=data["headers"])
        assert response.status_code == 201

        word = await Word.query.where(Word.name == "orange").gino.first()
        assert word
        assert word.description == "Test"

    @pytest.mark.asyncio
    async def test_add_word_present_in_db(
        self, client, data, use_db, mock_words_api_query_word
    ):
        word = await WordFactory(name="test")

        response = await client.post("/words/test", headers=data["headers"])
        assert response.status_code == 201

        word_from_db = await Word.query.where(
            Word.name == word.name
        ).gino.first()
        assert word_from_db.description == "Test"
        assert word_from_db.id == word.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize("word", ["banana", "apple", "fruit"])
    async def test_add_existing_word(
        self, word, client, data, use_db, mock_words_api_query_word
    ):
        response = await client.post(f"/words/{word}", headers=data["headers"])
        assert response.status_code == 409
