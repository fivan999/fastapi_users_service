from dishka import Provider, Scope, provide

from src.application.use_cases.users import UserUseCase
from src.domain.interfaces.password_manager import IPasswordManager
from src.domain.interfaces.repositories.users import IUserRepository
from src.domain.interfaces.tokens_manager import ITokenManager
from src.domain.interfaces.use_cases.users import IUserUseCase


class UserUseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(
        self,
        repository: IUserRepository,
        password_manager: IPasswordManager,
        token_manager: ITokenManager,
    ) -> IUserUseCase:
        return UserUseCase(repository, password_manager, token_manager)
