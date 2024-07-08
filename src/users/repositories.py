from src.users.schemes import UserCreateScheme, UserShowScheme, UserFullScheme
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models import User
from sqlalchemy.dialects.postgresql import insert
from src.users.utils.enums import UserEnum
from sqlalchemy import select, or_


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self, user_data: UserCreateScheme
    ) -> tuple[UserEnum, UserShowScheme | None]:
        async with self.session.begin():
            user_create_query = insert(User).values(
                **user_data.__dict__, hashed_password=user_data.password
            ).on_conflict_do_nothing().returning(User)
            new_user = await self.session.execute(user_create_query)
            new_user = new_user.scalar()
            await self.session.commit()
            if new_user is None:
                return UserEnum.USER_ALREADY_EXISTS, None
            return UserEnum.USER_CREATED, UserShowScheme(**new_user.__dict__)

    async def get_user_by_username_or_email(
        self, login: str
    ) -> tuple[UserEnum, UserFullScheme | None]:
        user_get_query = select(User).where(
            or_(User.username == login, User.email == login)
        )
        user_result = await self.session.execute(user_get_query)
        user_result = user_result.scalar()
        if user_result is None:
            return UserEnum.USER_NOT_EXISTS, None
        return UserEnum.USER_EXISTS, UserFullScheme(**user_result.__dict__)
