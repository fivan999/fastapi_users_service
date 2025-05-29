import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import Session

from src.application.services.password_manager import BcryptPasswordManager
from src.infrastructure.db.users.orm import User


@pytest.fixture(scope="function")
def user1(db_session: Session) -> User:
    user_obj = User(
        username="user1",
        email="user1@example.com",
        hashed_password=BcryptPasswordManager().hash_password("Paassword1"),
    )
    db_session.add(user_obj)
    db_session.commit()
    db_session.refresh(user_obj)
    return user_obj


@pytest_asyncio.fixture(scope="function")
async def access_and_refresh_token1(
    fastapi_test_client: AsyncClient, user1: User
) -> str:
    response = await fastapi_test_client.post(
        url="/users/login",
        json={"login": "user1", "password": "Paassword1"},
    )
    return response.json()
