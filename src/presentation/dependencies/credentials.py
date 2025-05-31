from dishka import Provider, Scope, provide
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.enums import TokenTypeEnum
from src.domain.interfaces.tokens_manager import ITokenManager
from src.presentation.dtos import UserIdDTO


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
        token_manager: ITokenManager,
    ) -> UserIdDTO:
        payload = token_manager.get_validated_token_data(
            credendials.credentials, TokenTypeEnum.ACCESS
        )
        return UserIdDTO(id=int(payload.get("sub")))
