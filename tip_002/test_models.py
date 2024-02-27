from typing import Callable
from uuid import uuid4

import pytest

from models import User


@pytest.fixture
def create_user() -> Callable[..., User]:
    def _create_user(**kwargs) -> User:
        user = User(
            id=kwargs.get("id", uuid4()),
            name=kwargs.get("name", "John Doe"),
            email=kwargs.get("email", "john@doe.com"),
            password=kwargs.get("password", "Secret123!"),
        )
        return user

    return _create_user


def test_password_must_be_at_least_8_characters(create_user: Callable[..., User]):
    with pytest.raises(ValueError):
        create_user(password="Sec123!")


def test_password_must_be_have_at_least_one_uppercase_letter(
    create_user: Callable[..., User],
):
    with pytest.raises(ValueError):
        create_user(password="secret123!")


def test_password_must_have_at_least_one_lowercase_letter(
    create_user: Callable[..., User],
):
    with pytest.raises(ValueError):
        create_user(password="SECRET123!")


def test_password_must_have_at_least_one_special_character(
    create_user: Callable[..., User],
):
    with pytest.raises(ValueError):
        create_user(password="Secret123")


def test_password_must_have_at_least_one_number(create_user: Callable[..., User]):
    with pytest.raises(ValueError):
        create_user(password="SecretSecret!")


def test_user_created_with_valid_password(create_user: Callable[..., User]):
    assert create_user(password="Secret123!").hashed_password
