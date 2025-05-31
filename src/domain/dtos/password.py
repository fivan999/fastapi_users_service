import string

from pydantic import BaseModel, field_validator


class PasswordDTO(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not 10 <= len(value) <= 50:
            raise ValueError("Password length should be from 10 to 50 symbols")
        symbols_set = set(value)
        if not any(i in symbols_set for i in string.digits):
            raise ValueError("Password shuold contain at least one digit")
        if not any(i in symbols_set for i in string.ascii_lowercase):
            raise ValueError(
                "Password shuold contain at least one lowercase latin letter"
            )
        if not any(i in symbols_set for i in string.ascii_uppercase):
            raise ValueError(
                "Password shuold contain at least one uppercase latin letter"
            )
        return value


class PasswordChangeDTO(PasswordDTO):
    old_password: str
