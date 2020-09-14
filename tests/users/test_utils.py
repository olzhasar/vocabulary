import pytest

from users.utils import hash_password


@pytest.mark.parametrize("password", ["123", "ASGIJASBOMAS", "90gjsjg0wu@!)($3gj3)"])
def test_hash_password(password):
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password
