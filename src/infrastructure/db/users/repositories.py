import datetime

from sqlalchemy import or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.dtos.users import UserCreateDTO, UserDTO
from src.domain.exceptions.users import (
    UserAlreadyExistsException,
    UserDoesNotExistException,
)
from src.domain.interfaces.repositories.users import IUserRepository
from src.infrastructure.db.users.orm import User


class PostgresUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user_data: UserCreateDTO) -> UserDTO:
        to_insert = user_data.__dict__
        to_insert["hashed_password"] = user_data.password
        del to_insert["password"]
        new_user = User(**to_insert)
        self.session.add(new_user)
        try:
            await self.session.flush()
            return UserDTO.model_validate(new_user, from_attributes=True)
        except IntegrityError as e:
            raise UserAlreadyExistsException() from e

    async def get_user_by_username_or_email(self, login: str) -> UserDTO:
        user_get_query = select(User).where(
            or_(User.username == login, User.email == login)
        )
        user_result = await self.session.execute(user_get_query)
        user_result = user_result.scalar()
        if user_result is None:
            raise UserDoesNotExistException()
        return UserDTO.model_validate(user_result, from_attributes=True)

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        user_get_query = select(User).where(User.id == user_id)
        user_result = await self.session.execute(user_get_query)
        user_result = user_result.scalar()
        if user_result is None:
            return UserDoesNotExistException()
        return UserDTO.model_validate(user_result, from_attributes=True)

    async def update_user_password(
        self, user_id: int, new_password: str
    ) -> None:
        password_update_query = (
            update(User)
            .where(User.id == user_id)
            .values(
                hashed_password=new_password,
                password_updated_at=datetime.datetime.now(
                    datetime.timezone.utc
                ),
            )
        )
        await self.session.execute(password_update_query)
        await self.session.flush()
