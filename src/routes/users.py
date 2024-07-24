from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from src.dependencies.users import CurrentUserDep, UserUseCaseDep
from src.schemes.password import PasswordChangeScheme
from src.schemes.tokens import AccessAndRefreshToken, AccessToken
from src.schemes.users import UserCreateScheme, UserLoginScheme, UserShowScheme
from src.utils.enums import UserEnum


user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/create', status_code=status.HTTP_201_CREATED)
async def user_create(
    user_data: UserCreateScheme, user_use_case: UserUseCaseDep
) -> UserShowScheme:
    creation_status, user_result_data = await user_use_case.create_user(
        user_data
    )
    if creation_status != UserEnum.USER_CREATED:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=creation_status.value,
        )
    return user_result_data


@user_router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(
    user_data: UserLoginScheme, user_use_case: UserUseCaseDep
) -> AccessAndRefreshToken:
    result_status, result_data = (
        await user_use_case.get_access_and_refresh_token(user_data)
    )
    if result_status != UserEnum.SUCCESS_LOGIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result_status.value,
        )
    return result_data


@user_router.post('/refresh', status_code=status.HTTP_200_OK)
async def get_new_access_token(
    refresh_token: Annotated[str, Body(embed=True)],
    user_use_case: UserUseCaseDep,
) -> AccessToken:
    result_status, token = (
        await user_use_case.get_new_access_token_by_refresh_token(
            refresh_token
        )
    )
    if result_status != UserEnum.TOKEN_IS_VALID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result_status.value,
        )
    return token


@user_router.get('/me', status_code=status.HTTP_200_OK)
async def get_user_profile(current_user: CurrentUserDep) -> UserShowScheme:
    return current_user


@user_router.get('/{username}', status_code=status.HTTP_200_OK)
async def get_user_by_username(
    username: str, user_use_case: UserUseCaseDep
) -> UserShowScheme:
    result_status, result_user = (
        await user_use_case.get_user_by_username_or_email(username)
    )
    if result_status != UserEnum.USER_EXISTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserEnum.USER_NOT_EXISTS.value,
        )
    return result_user


@user_router.post('/password/change', status_code=status.HTTP_200_OK)
async def change_user_password(
    current_user: CurrentUserDep,
    user_use_case: UserUseCaseDep,
    password_data: PasswordChangeScheme,
) -> dict:
    result_status = await user_use_case.update_user_password(
        current_user, password_data
    )
    if result_status != UserEnum.PASSWORD_CHANGED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result_status.value
        )
    return {'message': result_status.value}
