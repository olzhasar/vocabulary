import pytest
from sqlalchemy import and_

from api.auth import generate_access_token
from db.models import User, UserWord, Word
from db.tests.factories import UserFactory, WordFactory


@pytest.fixture
async def user():
    return await UserFactory(email="vincent@vega.com")


@pytest.fixture
async def headers(user):
    token = generate_access_token(user.email)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_words_api_query_word(mocker):
    mock = mocker.patch("api.views.words_api_client.query_word")
    return mock


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
async def test_word_list_ok(client, use_db, user, headers):
    words = ["banana", "peach", "watermelon"]
    for name in words:
        word = await Word.create(name=name)
        await UserWord.create(user_id=user.id, word_id=word.id)

    response = await client.get("/words", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_unexisting_word(
    use_db, auth_client, mock_words_api_query_word
):
    word = await Word.query.where(Word.name == "test").gino.first()
    assert not word

    mock_words_api_query_word.return_value = {"description": "test"}

    response = await auth_client.get("/search/test")
    assert response.status_code == 200

    mock_words_api_query_word.assert_called_once_with("test")
    assert response.json() == {"description": "test"}

    word = await Word.query.where(Word.name == "test").gino.first()
    assert word


@pytest.mark.asyncio
async def test_search_existing_word(
    use_db, auth_client, mock_words_api_query_word
):
    description = {"description": "test"}
    await WordFactory(name="fiction", description=description)

    response = await auth_client.get("/search/fiction")
    assert response.status_code == 200
    assert response.json() == description

    mock_words_api_query_word.assert_not_called()


@pytest.mark.asyncio
async def test_word_add_ok(
    use_db, client, user, headers, mock_words_api_query_word
):
    word = await WordFactory(name="orange")

    response = await client.post("/words/orange", headers=headers)
    assert response.status_code == 201

    user_word = await UserWord.query.where(
        and_(UserWord.user_id == user.id, UserWord.word_id == word.id)
    ).gino.first()
    assert user_word


@pytest.mark.asyncio
async def test_word_add_non_existing(
    use_db, client, user, headers, mock_words_api_query_word
):
    response = await client.post("/words/orange", headers=headers)
    assert response.status_code == 404
