import pytest
from pydantic import ValidationError

from schema import SignupSchema


def test_signup_schema():
    SignupSchema(
        **{
            "email": "info@test.com",
            "password": "Password123*",
            "repeat_password": "Password123*",
        }
    )

    with pytest.raises(ValidationError):
        SignupSchema(
            **{
                "email": "info@test.com",
                "password": "pass",
                "repeat_password": "pass",
            }
        )

    with pytest.raises(ValidationError):
        SignupSchema(
            **{
                "email": "info@test.com",
                "password": "Password123",
                "repeat_password": "Password321",
            }
        )
