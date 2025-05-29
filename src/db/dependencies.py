from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(
            url=f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
            echo=True,
            pool_size=100,
            max_overflow=0,
        )
        yield engine
        await engine.dispose()

    @provide
    def get_pool(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session
