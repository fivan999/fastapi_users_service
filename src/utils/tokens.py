import datetime
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidSignatureError

from src.config import settings
from src.utils.enums import UserEnum


def create_access_or_refresh_token(sub: str, token_type: str) -> str:
    data_to_encode = {'sub': sub, 'token_type': token_type}
    creation_time = datetime.datetime.now(datetime.timezone.utc)
    data_to_encode['iat'] = creation_time
    if token_type == 'access_token':
        data_to_encode['exp'] = creation_time + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    elif token_type == 'refresh_token':
        data_to_encode['exp'] = creation_time + datetime.timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    return jwt.encode(
        data_to_encode, settings.JWT_SECRET_KEY, algorithm='HS256'
    )


def decode_jwt_token(token: str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
    return payload


def get_validated_token_data(
    token: str, expected_token_type: str
) -> tuple[UserEnum, dict | None]:
    try:
        payload = decode_jwt_token(token)
    except ExpiredSignatureError:
        return UserEnum.TOKEN_EXPIRED, None
    except InvalidSignatureError:
        return UserEnum.INVALID_TOKEN, None
    username = payload.get('sub')
    token_type = payload.get('token_type')
    if (
        username is None
        or token_type is None
        or token_type != expected_token_type
    ):
        return UserEnum.INVALID_TOKEN, None
    return UserEnum.TOKEN_IS_VALID, payload


def get_jwt_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
) -> str:
    return credentials.credentials
