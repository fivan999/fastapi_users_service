from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.interfaces.uows.users import IUserUnitOfWork
from src.infrastructure.db.users.uow import PostgresUserUnitOfWork


class UserUnitOfWorkProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> IUserUnitOfWork:
        return PostgresUserUnitOfWork(sessionmaker)
