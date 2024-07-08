from src.users.repositories import UserRepository
from src.users.use_cases import UserUseCase
from fastapi import Depends
from src.db.dependencies import DatabaseDep
from typing import Annotated


async def get_user_repository(db: DatabaseDep) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def get_user_use_case(user_repository: UserRepositoryDep) -> UserUseCase:
    return UserUseCase(user_repository)


UserUseCaseDep = Annotated[UserUseCase, Depends(get_user_use_case)]
