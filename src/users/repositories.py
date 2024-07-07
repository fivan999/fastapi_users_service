from src.users.schemes import UserCreateScheme, UserScheme
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from src.users.models import User


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user_data: UserCreateScheme) -> UserScheme:
        hashed_password = pwd_context.hash(user_data.password)
        async with self.session.begin():
            user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password
            )
            self.session.add(user)
            await self.session.flush()
            return UserScheme(**user.__dict__)
