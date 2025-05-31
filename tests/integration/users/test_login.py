import datetime

import freezegun
import pytest
from httpx import AsyncClient

from src.config import settings
from src.infrastructure.db.users.orm import User


@pytest.mark.asyncio
async def test_success_login(
    fastapi_test_client: AsyncClient, user1: User
) -> None:
    response = await fastapi_test_client.post(
        url="/users/login",
        json={"login": "user1", "password": "Paassword1"},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert "access_token" in response_json
    assert "refresh_token" in response_json


@pytest.mark.asyncio
async def test_login_incorrect_username(
    fastapi_test_client: AsyncClient, user1: User
) -> None:
    response = await fastapi_test_client.post(
        url="/users/login",
        json={"login": "user2", "password": "Paassword1"},
    )
    response_json = response.json()
    assert response.status_code == 401
    assert "access_token" not in response_json
    assert "refresh_token" not in response_json


@pytest.mark.asyncio
async def test_login_incorrect_password(
    fastapi_test_client: AsyncClient, user1: User
) -> None:
    response = await fastapi_test_client.post(
        url="/users/login",
        json={"login": "user1", "password": "Paassword2"},
    )
    response_json = response.json()
    assert response.status_code == 401
    assert "access_token" not in response_json
    assert "refresh_token" not in response_json


@pytest.mark.asyncio
async def test_get_authorization_data_by_access_token(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: dict[str, str]
) -> None:
    access_token = access_and_refresh_token1.get("access_token", "fake")
    response = await fastapi_test_client.get(
        url="/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get("id") == 1


@pytest.mark.asyncio
async def test_get_access_token_by_refresh_token(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: dict[str, str]
) -> None:
    refresh_token = access_and_refresh_token1.get("refresh_token", "fake")
    response = await fastapi_test_client.post(
        url="/users/refresh", json={"refresh_token": refresh_token}
    )
    response_json = response.json()
    assert response.status_code == 200
    assert "access_token" in response_json


@pytest.mark.asyncio
async def test_get_authorization_by_invalid_access_token(
    fastapi_test_client: AsyncClient, user1: User
) -> None:
    response = await fastapi_test_client.get(
        url="/users/me", headers={"Authorization": "Bearer aboba"}
    )
    response_json = response.json()
    assert response.status_code == 401
    assert "id" not in response_json


@pytest.mark.asyncio
async def test_get_authorization_by_expired_access_token(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: User
) -> None:
    access_token = access_and_refresh_token1.get("access_token", "fake")
    mock_datetime = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS + 1)
    with freezegun.freeze_time(mock_datetime):
        response = await fastapi_test_client.get(
            url="/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
    response_json = response.json()
    assert response.status_code == 401
    assert "id" not in response_json


@pytest.mark.asyncio
async def test_get_access_token_by_expired_refresh_token(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: User
) -> None:
    refresh_token = access_and_refresh_token1.get("refresh_token", "fake")
    mock_datetime = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS + 1)
    with freezegun.freeze_time(mock_datetime):
        response = await fastapi_test_client.post(
            url="/users/refresh",
            json={"refresh_token": refresh_token},
        )
    response_json = response.json()
    assert response.status_code == 401
    assert "access_token" not in response_json


@pytest.mark.asyncio
async def test_login_after_password_change(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: User
) -> None:
    access_token = access_and_refresh_token1.get("access_token", "fake")
    response = await fastapi_test_client.post(
        url="/users/password/change",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"old_password": "Paassword1", "password": "Paassword2"},
    )
    response = await fastapi_test_client.post(
        url="/users/login",
        json={"login": "user1", "password": "Paassword2"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_new_access_token_with_old_refresh_after_password_change(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: User
) -> None:
    access_token = access_and_refresh_token1.get("access_token", "fake")
    with freezegun.freeze_time(
        datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=2)
    ):
        await fastapi_test_client.post(
            url="/users/password/change",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"old_password": "Paassword1", "password": "Paassword2"},
        )
    response = await fastapi_test_client.post(
        url="/users/refresh",
        json={
            "refresh_token": access_and_refresh_token1.get(
                "refresh_token", "fake"
            )
        },
    )
    response_json = response.json()
    assert response.status_code == 401
    assert "access_token" not in response_json
