from fastapi import APIRouter, HTTPException, status

from src.users.dependencies import CurrentUserDep, UserUseCaseDep
from src.users.schemes import (
    AccessAndRefreshToken,
    AccessToken,
    PasswordChangeScheme,
    UserCreateScheme,
    UserLoginScheme,
    UserShowScheme
)
from src.users.utils.enums import UserEnum
from src.users.utils.tokens import JWTTokenDep


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


@user_router.get('/refresh', status_code=status.HTTP_200_OK)
async def get_new_access_token(
    refresh_token: JWTTokenDep, user_use_case: UserUseCaseDep
) -> AccessToken:
    result_status, token = (
        await user_use_case.get_new_access_token_by_refresh_token(
            refresh_token
        )
    )
    if result_status != UserEnum.TOKEN_IS_VALID:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result_status.value,
        )
    return token


@user_router.get('/me', status_code=status.HTTP_200_OK)
async def get_user_profile(current_user: CurrentUserDep) -> UserShowScheme:
    return current_user


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
