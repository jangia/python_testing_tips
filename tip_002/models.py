from uuid import UUID

import bcrypt
from pydantic import BaseModel, field_validator, Field, EmailStr


class User(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    hashed_password: str = Field(..., alias="password")

    @field_validator("hashed_password", mode="before")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters")

        if not any(char.isupper() for char in value):
            raise ValueError("password must have at least one uppercase letter")

        if not any(char.islower() for char in value):
            raise ValueError("password must have at least one lowercase letter")

        if not any(char in "!@#$%^&*()" for char in value):
            raise ValueError(
                "password must have at least one special character: !@#$%^&*()"
            )

        if not any(char.isdigit() for char in value):
            raise ValueError("password must have at least one number")

        return bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
