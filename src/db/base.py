from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings


engine = create_async_engine(
    url=f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}'
    f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}',
    echo=True,
)
Base = declarative_base()
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
