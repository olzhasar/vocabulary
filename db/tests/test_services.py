import pytest

from db.models import UserWord, Word, WordVariant
from db.services import add_new_word, get_user_words_with_variants
from db.tests.factories import UserFactory, WordFactory


@pytest.mark.asyncio
async def test_add_new_word(use_db):
    word = await add_new_word(
        "chair",
        variants=[
            {"part_of_speech": "noun", "definition": "definition_1"},
            {
                "part_of_speech": "adjective",
                "definition": "definition_2",
            },
        ],
    )

    assert isinstance(word, Word)

    word_from_db = await Word.query.where(Word.name == "chair").gino.first()
    assert word_from_db.id == word.id

    variants = await WordVariant.load(word=Word).gino.all()

    assert variants[0].word_id == word.id
    assert variants[0].part_of_speech == "noun"
    assert variants[0].definition == "definition_1"

    assert variants[1].word_id == word.id
    assert variants[1].part_of_speech == "adjective"
    assert variants[1].definition == "definition_2"


@pytest.mark.asyncio
async def test_get_user_words_with_variants(use_db):
    user = await UserFactory()

    words = ["banana", "peach", "watermelon"]
    for name in words:
        word = await WordFactory(
            name=name,
            variants=[
                dict(part_of_speech="noun", definition="test1"),
                dict(part_of_speech="adjective", definition="test2"),
            ],
        )
        await UserWord.create(user_id=user.id, word_id=word.id)

    words_from_db = await get_user_words_with_variants(user.id)

    assert len(words_from_db) == len(words)

    for i, word in enumerate(words_from_db):
        assert word.name == words[i]
        assert word.variants[0].part_of_speech == "noun"
        assert word.variants[0].definition == "test1"
        assert word.variants[1].part_of_speech == "adjective"
        assert word.variants[1].definition == "test2"
