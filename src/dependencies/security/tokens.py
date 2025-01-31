from dishka import Provider, Scope, provide

from src.utils.security.tokens import JwtTokenManager


class JwtTokenManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_jwt_token_manager(self) -> JwtTokenManager:
        return JwtTokenManager()
