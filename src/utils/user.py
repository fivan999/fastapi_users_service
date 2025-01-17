from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import UserRepository
from src.use_cases.users import UserUseCase


async def get_user_use_case(db: AsyncSession) -> UserUseCase:
    return UserUseCase(UserRepository(db))
