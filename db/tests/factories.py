import factory

from db.models import User


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
