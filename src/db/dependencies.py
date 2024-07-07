from src.db.base import async_session
from typing import AsyncGenerator


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session
