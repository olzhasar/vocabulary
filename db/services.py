from typing import Dict, List

from .models import Word, WordVariant


async def add_new_word(name: str, variants: List[Dict[str, str]]):
    word = await Word.create(name=name)

    for variant in variants:
        await WordVariant.create(word_id=word.id, **variant)

    return word
