from fastapi import APIRouter
from src.users.schemes import UserCreateScheme, UserShowScheme, UserLoginScheme, AccessAndRefreshToken
from fastapi import status
from src.users.dependencies import UserUseCaseDep
from src.users.utils.enums import UserEnum
from fastapi import HTTPException


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
            detail=creation_status
        )
    return user_result_data


@user_router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(
    user_data: UserLoginScheme, user_use_case: UserUseCaseDep
) -> AccessAndRefreshToken:
    result_status, result_data = await user_use_case.user_login(user_data)
    if result_status != UserEnum.SUCCESS_LOGIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result_status,
        )
    return result_data
