import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "data, status_code",
    [
        # correct
        (
            {
                "username": "user1",
                "password": "Paassword1",
                "email": "ex@mail.com",
            },
            201,
        ),
        # correct
        (
            {
                "username": "user1",
                "password": "Paassword1&&&&",
                "email": "ex@mail.com",
            },
            201,
        ),
        # too long username
        (
            {
                "username": "usjjjjjjjjjjffffffffffffffffffffffjjjjjjjjjjjjjjjjjjjser1",
                "password": "Paassword1",
                "email": "ex@mail.com",
            },
            400,
        ),
        # too short username
        (
            {
                "username": "usr1",
                "password": "Paassword1",
                "email": "ex@mail.com",
            },
            400,
        ),
        # special symbols in username
        (
            {
                "username": "user1%",
                "password": "Paassword1",
                "email": "ex@mail.com",
            },
            400,
        ),
        # incorrect email
        (
            {
                "username": "user1",
                "password": "Paassword1",
                "email": "exmail.com",
            },
            400,
        ),
        # no uppercase in password
        (
            {
                "username": "user1",
                "password": "paassword1",
                "email": "ex@mail.com",
            },
            400,
        ),
        # no digit in password
        (
            {
                "username": "user1",
                "password": "Paasswordd",
                "email": "ex@mail.com",
            },
            400,
        ),
        # no lowercase in password
        (
            {
                "username": "user1",
                "password": "PAASSWORD1",
                "email": "ex@mail.com",
            },
            400,
        ),
        # too short password
        (
            {
                "username": "user1",
                "password": "Pass1",
                "email": "ex@mail.com",
            },
            400,
        ),
        # too long password
        (
            {
                "username": "user1",
                "password": "Paaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaass1",
                "email": "ex@mail.com",
            },
            400,
        ),
    ],
)
@pytest.mark.asyncio
async def test_user_creation(
    fastapi_test_client: AsyncClient, data: dict, status_code: int
) -> None:
    response = await fastapi_test_client.post(
        url="/users/create",
        json=data,
    )
    assert response.status_code == status_code
