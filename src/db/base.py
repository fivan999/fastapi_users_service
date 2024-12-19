from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings


Base = declarative_base()


async def init_database() -> async_sessionmaker:
    """
    Creating db sessions' factory

    Returns:
        async_sessionmaker: session factory
    """
    engine = create_async_engine(
        url=f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
        f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}',
        echo=True,
    )
    return async_sessionmaker(engine, expire_on_commit=False)
