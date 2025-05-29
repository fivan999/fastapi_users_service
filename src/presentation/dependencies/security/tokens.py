from dishka import Provider, Scope, provide

from src.application.services.jwt_tokens_manager import JwtTokenManager
from src.domain.interfaces.tokens_manager import ITokenManager


class JwtTokenManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_jwt_token_manager(self) -> ITokenManager:
        return JwtTokenManager()
