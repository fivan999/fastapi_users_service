from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.main import app


@pytest_asyncio.fixture(scope='function')
async def fastapi_test_client(
    async_db_sessionmaker: async_sessionmaker, db_clean
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        app.state.async_sessionmaker = async_db_sessionmaker
        yield client
