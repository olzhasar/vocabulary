from typing import Dict, List

from sqlalchemy import and_

from .models import UserWord, Word, WordVariant


async def add_new_word(name: str, variants: List[Dict[str, str]]):
    word = await Word.create(name=name)

    for variant in variants:
        word.add_variant = await WordVariant.create(word_id=word.id, **variant)

    return word


async def get_word_with_variants_by_name(name: str):
    result = (
        await Word.distinct(Word.id)
        .load(add_variant=WordVariant)
        .query.where(Word.name == name)
        .gino.all()
    )

    if result:
        return result[0]

    return None


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


async def get_user_word(word_id: int, user_id: int):
    return await UserWord.query.where(
        and_(UserWord.word_id == word_id, UserWord.user_id == user_id)
    ).gino.first()
