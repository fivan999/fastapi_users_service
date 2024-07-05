from config import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker


engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True,
)
Base = declarative_base()
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
