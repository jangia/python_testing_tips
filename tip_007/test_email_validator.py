import pytest

from email_validator import is_valid_email


@pytest.mark.parametrize(
    "email",
    [
        "bob@builder.com",
        "bob.builder@builder.org",
        "bob+test@builder.com",
        "bob.o'builder@builder.com"
    ]
)
def test_email_is_valid(email: str):
    assert is_valid_email(email) is True


@pytest.mark.parametrize(
    "email",
    [
        "random string without @",
        "domain.com",
        "bob@builder",
        "@builder.com",
    ]
)
def test_email_is_not_valid(email: str):
    assert is_valid_email(email) is False