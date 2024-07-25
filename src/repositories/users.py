import datetime

from sqlalchemy import or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.schemes.users import UserCreateScheme, UserFullScheme, UserShowScheme
from src.utils.enums import UserEnum


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        """
        Initializing of user repository

        Args:
            session (AsyncSession): async db session
        """
        self.session = session

    async def create_user(
        self, user_data: UserCreateScheme
    ) -> tuple[UserEnum, UserShowScheme | None]:
        """
        Creating a user with user's data

        Args:
            user_data (UserCreateScheme): scheme with user's data

        Returns:
            tuple[
                UserEnum, UserShowScheme | None
            ]: enum with state and user's data
        """
        async with self.session.begin():
            to_insert = user_data.__dict__
            to_insert['hashed_password'] = user_data.password
            del to_insert['password']
            user_create_query = (
                insert(User)
                .values(**to_insert)
                .on_conflict_do_nothing()
                .returning(User)
            )
            new_user = await self.session.execute(user_create_query)
            new_user = new_user.scalar()
            await self.session.commit()
        if new_user is None:
            return UserEnum.USER_ALREADY_EXISTS, None
        return UserEnum.USER_CREATED, UserShowScheme(**new_user.__dict__)

    async def get_user_by_username_or_email(
        self, login: str
    ) -> tuple[UserEnum, UserFullScheme | None]:
        """
        Getting user data by username or email

        Args:
            login (str): email or username of a user

        Returns:
            tuple[
                UserEnum, UserFullScheme | None
            ]: enum with state and user's data
        """
        user_get_query = select(User).where(
            or_(User.username == login, User.email == login)
        )
        user_result = await self.session.execute(user_get_query)
        user_result = user_result.scalar()
        if user_result is None:
            return UserEnum.USER_NOT_EXISTS, None
        return UserEnum.USER_EXISTS, UserFullScheme(**user_result.__dict__)

    async def update_user_password(
        self, username: str, new_password: str
    ) -> UserEnum:
        """
        Update user's password

        Args:
            username (str)
            new_password (str)

        Returns:
            UserEnum: status of updating password
        """
        password_update_query = (
            update(User)
            .where(User.username == username)
            .values(
                hashed_password=new_password,
                password_updated_at=datetime.datetime.now(
                    datetime.timezone.utc
                ),
            )
        )
        await self.session.execute(password_update_query)
        await self.session.commit()
        return UserEnum.PASSWORD_CHANGED
