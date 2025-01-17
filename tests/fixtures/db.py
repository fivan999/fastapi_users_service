from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import settings
from tests.utils.db import clear_db_tables, recreate_db_tables


@pytest.fixture(scope='session')
def db_engine() -> Engine:
    engine = create_engine(
        url=f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
        echo=True,
        pool_size=100,
        max_overflow=0,
    )
    recreate_db_tables(engine)
    return engine


@pytest.fixture(scope='session')
def db_sessionmaker(
    db_engine: Engine,
) -> sessionmaker:
    db_sessionmaker = sessionmaker(
        db_engine, autoflush=False, autocommit=False, expire_on_commit=False
    )
    return db_sessionmaker


@pytest_asyncio.fixture(scope='function')
async def async_db_sessionmaker() -> async_sessionmaker:
    engine = create_async_engine(
        url=f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
        echo=True,
    )
    return async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False, autocommit=False
    )


@pytest.fixture(scope='function')
def db_session(
    db_sessionmaker: sessionmaker,
) -> Generator[Session, None, None]:
    session = db_sessionmaker()
    yield session


@pytest.fixture(scope='function')
def db_clean(
    db_sessionmaker: sessionmaker,
) -> None:
    clear_db_tables(db_sessionmaker)
