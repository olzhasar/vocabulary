import pytest

from db.models import Word, WordVariant
from db.tests.factories import WordFactory


@pytest.mark.asyncio
async def test_word_factory(use_db):
    word = await WordFactory(
        name="chair",
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
