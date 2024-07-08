from src.db.base import async_session
from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
