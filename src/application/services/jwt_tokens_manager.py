import datetime
from enum import Enum

import jwt
from jwt import ExpiredSignatureError, PyJWTError

from src.config import settings
from src.domain.enums import TokenTypeEnum
from src.domain.exceptions.tokens import (
    InvalidTokenException,
    TokenExpiredException,
)
from src.domain.interfaces.tokens_manager import ITokenManager


class JwtTokenManager(ITokenManager):
    def create_token(self, sub: str, token_type: TokenTypeEnum) -> str:
        data_to_encode = {"sub": sub, "token_type": token_type.value}
        creation_time = datetime.datetime.now(datetime.timezone.utc)
        data_to_encode["iat"] = creation_time
        if token_type == TokenTypeEnum.ACCESS:
            data_to_encode["exp"] = creation_time + datetime.timedelta(
                seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
            )
        elif token_type == TokenTypeEnum.REFRESH:
            data_to_encode["exp"] = creation_time + datetime.timedelta(
                seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
            )
        return jwt.encode(
            data_to_encode, settings.JWT_SECRET_KEY, algorithm="HS256"
        )

    def decode_token(self, token: str) -> dict:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        return payload

    def get_validated_token_data(
        self, token: str, expected_token_type: TokenTypeEnum
    ) -> dict:
        try:
            payload = self.decode_token(token)
        except ExpiredSignatureError as e:
            raise TokenExpiredException() from e
        except PyJWTError as e:
            raise InvalidTokenException() from e
        user_id = payload.get("sub")
        token_type = payload.get("token_type")
        if (
            user_id is None
            or token_type is None
            or token_type != expected_token_type.value
        ):
            raise InvalidTokenException()
        return payload
