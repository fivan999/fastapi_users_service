from src.users.repositories import UserRepository
from src.users.use_cases import UserUseCase
from fastapi import Depends
from src.db.dependencies import DatabaseDep
from typing import Annotated
from fastapi import HTTPException
from fastapi import status
from src.users.schemes import UserFullScheme
from src.users.utils.enums import UserEnum
from src.users.utils.tokens import JWTTokenDep


async def get_user_repository(db: DatabaseDep) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def get_user_use_case(user_repository: UserRepositoryDep) -> UserUseCase:
    return UserUseCase(user_repository)


UserUseCaseDep = Annotated[UserUseCase, Depends(get_user_use_case)]


async def get_current_user_by_access_token(
    token: JWTTokenDep,
    user_use_case: UserUseCaseDep
) -> UserFullScheme:
    result_status, result_user = await user_use_case.get_user_by_access_token(
        token
    )
    if result_status != UserEnum.USER_EXISTS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result_status.value
        )
    return result_user


CurrentUserDep = Annotated[dict, Depends(get_current_user_by_access_token)]
