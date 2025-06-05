from dishka import Provider, Scope, provide

from src.application.use_cases.users import UserUseCase
from src.domain.interfaces.password_manager import IPasswordManager
from src.domain.interfaces.tokens_manager import ITokenManager
from src.domain.interfaces.uows.users import IUserUnitOfWork
from src.domain.interfaces.use_cases.users import IUserUseCase


class UserUseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(
        self,
        uow: IUserUnitOfWork,
        password_manager: IPasswordManager,
        token_manager: ITokenManager,
    ) -> IUserUseCase:
        return UserUseCase(uow, password_manager, token_manager)
