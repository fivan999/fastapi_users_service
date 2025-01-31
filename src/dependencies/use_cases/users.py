from dishka import Provider, Scope, provide

from src.repositories.users import UserRepository
from src.use_cases.users import UserUseCase
from src.utils.security.password import PasswordManager
from src.utils.security.tokens import JwtTokenManager


class UserUseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(
        self,
        repository: UserRepository,
        password_manager: PasswordManager,
        token_manager: JwtTokenManager,
    ) -> UserUseCase:
        return UserUseCase(repository, password_manager, token_manager)
