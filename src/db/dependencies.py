from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import async_session


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
