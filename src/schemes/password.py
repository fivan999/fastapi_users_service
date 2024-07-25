from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class PasswordScheme(BaseModel):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        """
        Validating a password

        Args:
            value (str): password

        Raises:
            HTTPException: password is invalid

        Returns:
            str: validated password
        """
        if len(value) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='password should be at least 8 symbols long',
            )
        return value


class PasswordChangeScheme(PasswordScheme):
    old_password: str
