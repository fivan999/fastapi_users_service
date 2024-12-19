import datetime
import re

from pydantic import BaseModel, EmailStr, field_validator

from src.schemes.password import PasswordScheme


class UserBaseScheme(BaseModel):
    username: str
    email: EmailStr


class UserCreateScheme(UserBaseScheme, PasswordScheme):
    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        """
        Validate a username

        Args:
            value (str): username

        Raises:
            HTTPException: user is invalid

        Returns:
            str: validated username
        """
        if not 5 <= len(value) <= 30:
            raise ValueError(
                'username must be 5 to 30 symbols length',
            )
        if not re.fullmatch(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError(
                'username must consist only of english '
                'letters, digits and _ sign',
            )
        return value


class UserShowScheme(UserBaseScheme):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserFullScheme(UserShowScheme):
    hashed_password: str
    password_updated_at: datetime.datetime

    class Config:
        from_attributes = True


class UserLoginScheme(BaseModel):
    login: str
    password: str
