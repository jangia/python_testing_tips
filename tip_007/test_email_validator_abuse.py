import pytest

from email_validator import is_valid_email


@pytest.mark.parametrize(
    "email,is_valid",
    [
        ("bob@builder.com", True),
        ("gqehtjwyeumi,", False),
    ]
)
def test_is_valid_email(email: str, is_valid: bool):
    assert is_valid_email(email) == is_valid


@pytest.mark.parametrize(
    "email,is_valid",
    [
        ("bob@builder.com", True),
        ("gqehtjwyeumi,", False),
    ]
)
def test_is_valid_email(email: str, is_valid: bool):
    if is_valid:
        assert is_valid_email(email) is True
    else:
        assert is_valid_email(email) is False