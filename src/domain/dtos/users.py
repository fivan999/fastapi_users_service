import datetime
import re
from typing import ClassVar

from pydantic import BaseModel, EmailStr, field_validator

from src.domain.dtos.password import PasswordDTO


class UserBaseDTO(BaseModel):
    username: str
    email: EmailStr


class UserCreateDTO(UserBaseDTO, PasswordDTO):
    USERNAME_PATTERN: ClassVar = re.compile(r"^[a-zA-Z0-9_]+$")

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not 5 <= len(value) <= 30:
            raise ValueError(
                "username must be 5 to 30 symbols length",
            )
        if not cls.USERNAME_PATTERN.match(value):
            raise ValueError(
                "username must consist only of english "
                "letters, digits and _ sign",
            )
        return value


class UserReadDTO(UserBaseDTO):
    id: int
    is_active: bool


class UserDTO(UserReadDTO):
    hashed_password: str
    password_updated_at: datetime.datetime


class UserLoginDTO(BaseModel):
    login: str
    password: str
