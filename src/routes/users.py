from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, HTTPException, status

from src.schemes.errors import ErrorScheme
from src.schemes.password import PasswordChangeScheme
from src.schemes.tokens import AccessAndRefreshToken, AccessToken
from src.schemes.users import (
    UserCreateScheme,
    UserIdScheme,
    UserLoginScheme,
    UserShowScheme,
)
from src.use_cases.users import UserUseCase
from src.utils.enums import AuthEnum, TokenEnum, UserEnum


user_router = APIRouter(
    prefix='/users', tags=['Users'], route_class=DishkaRoute
)


@user_router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Created user'},
        400: {'description': 'Bad request', 'model': ErrorScheme},
    },
)
async def user_create(
    user_data: UserCreateScheme, user_use_case: FromDishka[UserUseCase]
) -> UserShowScheme:
    creation_status, user_result_data = await user_use_case.create_user(
        user_data
    )
    if creation_status != UserEnum.USER_CREATED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=creation_status.value,
        )
    return user_result_data


@user_router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    responses={
        200: {'description': 'Refresh and access token'},
        401: {'description': 'Invalid user data', 'model': ErrorScheme},
    },
)
async def user_login(
    user_data: UserLoginScheme, user_use_case: FromDishka[UserUseCase]
) -> AccessAndRefreshToken:
    result_status, result_data = (
        await user_use_case.get_access_and_refresh_token(user_data)
    )
    if result_status != AuthEnum.SUCCESS_LOGIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result_status.value,
        )
    return result_data


@user_router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    responses={
        200: {'description': 'New access token'},
        403: {'description': 'Invalid refresh token', 'model': ErrorScheme},
    },
)
async def get_new_access_token(
    refresh_token: Annotated[str, Body(embed=True)],
    user_use_case: FromDishka[UserUseCase],
) -> AccessToken:
    result_status, token = (
        await user_use_case.get_new_access_token_by_refresh_token(
            refresh_token
        )
    )
    if result_status != TokenEnum.TOKEN_IS_VALID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result_status.value,
        )
    return token


@user_router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    responses={
        200: {'description': 'User data'},
        401: {'description': 'Unauthorized', 'model': ErrorScheme},
        403: {"description": "Credentials not provided", "model": ErrorScheme},
        404: {"description": "User not found", "model": ErrorScheme},
    },
)
async def get_user_profile(
    user_id_scheme: FromDishka[UserIdScheme],
    user_use_case: FromDishka[UserUseCase],
) -> UserShowScheme:
    user_status, user_data = await user_use_case.get_user_by_id(
        user_id_scheme.id
    )
    if user_status != UserEnum.USER_EXISTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user_data


@user_router.post(
    '/password/change',
    status_code=status.HTTP_200_OK,
    responses={
        200: {'description': 'Successful'},
        401: {'description': 'Unauthorized', 'model': ErrorScheme},
        400: {
            'description': 'Invalid old or new password',
            'model': ErrorScheme,
        },
    },
)
async def change_user_password(
    user_id_scheme: FromDishka[UserIdScheme],
    user_use_case: FromDishka[UserUseCase],
    password_data: PasswordChangeScheme,
) -> dict:
    result_status = await user_use_case.update_user_password(
        user_id_scheme.id, password_data
    )
    if result_status != AuthEnum.PASSWORD_CHANGED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result_status.value
        )
    return {'message': result_status.value}
