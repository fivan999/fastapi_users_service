from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interfaces.repositories.users import IUserRepository
from src.infrastructure.db.users.repositories import PostgresUserRepository


class UserRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(
        self, session: AsyncSession
    ) -> IUserRepository:
        return PostgresUserRepository(session)
