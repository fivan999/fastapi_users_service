from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.interfaces.uows.users import IUserUnitOfWork
from src.infrastructure.db.users.repositories import PostgresUserRepository


class PostgresUserUnitOfWork(IUserUnitOfWork):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.sessionmaker = sessionmaker

    @asynccontextmanager
    async def start(self):
        self.session: AsyncSession = self.sessionmaker()
        self.users = PostgresUserRepository(self.session)
        try:
            yield self
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
        finally:
            await self.session.close()
