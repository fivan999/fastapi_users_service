from dishka import Provider, Scope, provide
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from src.schemes.users import UserIdScheme
from src.utils.enums import TokenEnum, TokenTypeEnum
from src.utils.security.tokens import JwtTokenManager


class CredentialsProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_access_token(
        self, request: Request
    ) -> HTTPAuthorizationCredentials:
        return await HTTPBearer()(request)

    @provide
    async def get_user_id(
        self,
        credendials: HTTPAuthorizationCredentials,
        token_manager: JwtTokenManager,
    ) -> UserIdScheme:
        token_status, payload = token_manager.get_validated_token_data(
            credendials.credentials, TokenTypeEnum.ACCESS
        )
        if token_status != TokenEnum.TOKEN_IS_VALID:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=token_status.value,
            )
        return UserIdScheme(id=int(payload.get("sub")))
