from typing import Dict, List

from .models import UserWord, Word, WordVariant


async def add_new_word(name: str, variants: List[Dict[str, str]]):
    word = await Word.create(name=name)

    for variant in variants:
        await WordVariant.create(word_id=word.id, **variant)

    return word


async def get_user_words_with_variants(user_id: int):
    user_words = (
        UserWord.select("word_id")
        .where(UserWord.user_id == user_id)
        .as_scalar()
    )

    return (
        await Word.distinct(Word.id)
        .load(add_variant=WordVariant)
        .query.where(Word.id.in_(user_words))
        .gino.all()
    )
