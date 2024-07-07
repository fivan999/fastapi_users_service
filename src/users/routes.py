from fastapi import APIRouter, Depends
from src.users.schemes import UserCreateScheme, UserScheme
from src.db.dependencies import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.repositories import UserRepository
from fastapi import status


user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/create', status_code=status.HTTP_201_CREATED)
async def user_create(
    user_data: UserCreateScheme, db: Annotated[AsyncSession, Depends(get_db)]
) -> UserScheme:
    user_repository = UserRepository(db)
    return await user_repository.create_user(user_data)
