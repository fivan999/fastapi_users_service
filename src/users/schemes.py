import datetime
import re

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator


class UserBaseScheme(BaseModel):
    username: str
    email: EmailStr


class PasswordScheme(BaseModel):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='password should be at least 8 symbols long',
            )
        return value


class UserCreateScheme(UserBaseScheme, PasswordScheme):
    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not 5 <= len(value) <= 30:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='username must be 5 to 30 symbols length',
            )
        if not re.fullmatch(r'^[a-zA-Z0-9_]+$', value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='username must consist only of english '
                'letters, digits and _ sign',
            )
        return value


class UserShowScheme(UserBaseScheme):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserFullScheme(UserShowScheme):
    hashed_password: str
    password_updated_at: datetime.datetime

    class Config:
        orm_mode = True


class UserLoginScheme(BaseModel):
    login: str
    password: str


class AccessToken(BaseModel):
    access_token: str


class AccessAndRefreshToken(AccessToken):
    refresh_token: str


class PasswordChangeScheme(PasswordScheme):
    old_password: str
