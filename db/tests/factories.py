import random
import string

import factory

from db.models import User, Word


def get_random_string(instance):
    letters = string.ascii_lowercase
    _range = range(random.randint(4, 20))
    return "".join(random.choice(letters) for i in _range)


class UserFactory(factory.Factory):
    email = factory.sequence(lambda n: f"test_{n}@example.com")
    password = "123qweasd"

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create_async(*args, **kwargs):
            return await model_class.register(*args, **kwargs)

        return create_async(*args, **kwargs)


class WordFactory(factory.Factory):
    name = factory.LazyAttribute(get_random_string)

    class Meta:
        model = Word

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create_async(*args, **kwargs):
            return await model_class.create(*args, **kwargs)

        return create_async(*args, **kwargs)
