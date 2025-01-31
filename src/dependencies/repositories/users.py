from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import UserRepository


class UserRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(
        self, session: AsyncSession
    ) -> UserRepository:
        return UserRepository(session)
