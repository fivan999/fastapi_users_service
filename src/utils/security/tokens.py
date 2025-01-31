import datetime
from enum import Enum

import jwt
from jwt import ExpiredSignatureError, PyJWTError

from src.config import settings
from src.utils.enums import TokenEnum, TokenTypeEnum


class JwtTokenManager:
    @classmethod
    def create_access_or_refresh_token(
        cls, sub: str, token_type: TokenTypeEnum
    ) -> str:
        """
        Creating a jwt token with

        Args:
            sub (str): useful data
            token_type (str): type of a token (access or refresh)

        Returns:
            str: jwt token
        """
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

    @classmethod
    def decode_jwt_token(cls, token: str) -> dict:
        """
        Getting payload of a jwt token

        Args:
            token (str): jwt token

        Returns:
            dict: payload
        """
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        return payload

    @classmethod
    def get_validated_token_data(
        cls, token: str, expected_token_type: TokenTypeEnum
    ) -> tuple[Enum, dict | None]:
        """
        Validate jwt token and get payload

        Args:
            token (str): jwt token
            expected_token_type (str): type of a token (access or refresh)

        Returns:
            tuple[UserEnum, dict | None]: Enum with status and payload
        """
        try:
            payload = cls.decode_jwt_token(token)
        except ExpiredSignatureError:
            return TokenEnum.TOKEN_EXPIRED, None
        except PyJWTError:
            return TokenEnum.INVALID_TOKEN, None
        user_id = payload.get("sub")
        token_type = payload.get("token_type")
        if (
            user_id is None
            or token_type is None
            or token_type != expected_token_type.value
        ):
            return TokenEnum.INVALID_TOKEN, None
        return TokenEnum.TOKEN_IS_VALID, payload
