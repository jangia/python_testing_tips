from uuid import uuid4

import pytest

from models import User


def test_password_must_be_at_least_8_characters():
    with pytest.raises(ValueError):
        User(id=uuid4(), name="John Doe", email="john@doe.com", password="Sec123!")


def test_password_must_be_have_at_least_one_uppercase_letter():
    with pytest.raises(ValueError):
        User(id=uuid4(), name="John Doe", email="john@doe.com", password="secret123!")


def test_password_must_have_at_least_one_lowercase_letter():
    with pytest.raises(ValueError):
        User(id=uuid4(), name="John Doe", email="john@doe.com", password="SECRET123!")


def test_password_must_have_at_least_one_special_character():
    with pytest.raises(ValueError):
        User(id=uuid4(), name="John Doe", email="john@doe.com", password="Secret123")


def test_password_must_have_at_least_one_number():
    with pytest.raises(ValueError):
        User(id=uuid4(), name="John Doe", email="john@doe.com", password="SecretSecret!")


def test_user_created_with_valid_password():
    assert User(id=uuid4(), name="John Doe", email="john@doe.com", password="Secret123!").hashed_password