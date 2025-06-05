from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, status
from fastapi.responses import Response

from src.domain.dtos.password import PasswordChangeDTO
from src.domain.dtos.tokens import AccessAndRefreshTokenDTO, AccessTokenDTO
from src.domain.dtos.users import UserCreateDTO, UserLoginDTO, UserReadDTO
from src.domain.interfaces.use_cases.users import IUserUseCase
from src.presentation.dtos import HttpErrorDTO, UserIdDTO


user_router = APIRouter(
    prefix="/users", tags=["Users"], route_class=DishkaRoute
)


@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Created user"},
        400: {"description": "Bad request", "model": HttpErrorDTO},
    },
)
async def user_create(
    user_data: UserCreateDTO, user_use_case: FromDishka[IUserUseCase]
) -> UserReadDTO:
    return await user_use_case.create_user(user_data)


@user_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Refresh and access token"},
        401: {"description": "Invalid user data", "model": HttpErrorDTO},
    },
)
async def user_login(
    user_data: UserLoginDTO, user_use_case: FromDishka[IUserUseCase]
) -> AccessAndRefreshTokenDTO:
    return await user_use_case.get_access_and_refresh_token(user_data)


@user_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "New access token"},
        403: {"description": "Invalid refresh token", "model": HttpErrorDTO},
    },
)
async def get_new_access_token(
    refresh_token: Annotated[str, Body(embed=True)],
    user_use_case: FromDishka[IUserUseCase],
) -> AccessTokenDTO:
    return await user_use_case.get_new_access_token_by_refresh_token(
        refresh_token
    )


@user_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User data"},
        401: {"description": "Unauthorized", "model": HttpErrorDTO},
        403: {
            "description": "Credentials not provided",
            "model": HttpErrorDTO,
        },
        404: {"description": "User not found", "model": HttpErrorDTO},
    },
)
async def get_user_profile(
    user_id_scheme: FromDishka[UserIdDTO],
    user_use_case: FromDishka[IUserUseCase],
) -> UserReadDTO:
    return await user_use_case.get_user_by_id(user_id_scheme.id)


@user_router.post(
    "/password/change",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful"},
        401: {"description": "Unauthorized", "model": HttpErrorDTO},
        400: {
            "description": "Invalid old or new password",
            "model": HttpErrorDTO,
        },
    },
)
async def change_user_password(
    user_id_scheme: FromDishka[UserIdDTO],
    user_use_case: FromDishka[IUserUseCase],
    password_data: PasswordChangeDTO,
) -> Response:
    await user_use_case.update_user_password(user_id_scheme.id, password_data)
    return Response(status_code=status.HTTP_200_OK)
