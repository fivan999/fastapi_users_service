import datetime

from src.domain.dtos.password import PasswordChangeDTO
from src.domain.dtos.tokens import AccessAndRefreshTokenDTO, AccessTokenDTO
from src.domain.dtos.users import UserCreateDTO, UserDTO, UserLoginDTO
from src.domain.enums import TokenTypeEnum
from src.domain.exceptions.auth import (
    InvalidCredentialsException,
    PasswordChangedException,
    WrongPasswordException,
)
from src.domain.exceptions.users import (
    UserDoesNotExistException,
    UserIsNotActiveException,
)
from src.domain.interfaces.password_manager import IPasswordManager
from src.domain.interfaces.repositories.users import IUserRepository
from src.domain.interfaces.tokens_manager import ITokenManager
from src.domain.interfaces.use_cases.users import IUserUseCase


class UserUseCase(IUserUseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
        password_manager: IPasswordManager,
        token_manager: ITokenManager,
    ) -> None:
        self.user_repository = user_repository
        self.password_manager = password_manager
        self.token_manager = token_manager

    async def create_user(self, user_data: UserCreateDTO) -> UserDTO:
        user_data.password = self.password_manager.hash_password(
            user_data.password
        )
        return await self.user_repository.create_user(user_data)

    async def get_user_by_username_or_email(self, login: str) -> UserDTO:
        return await self.user_repository.get_user_by_username_or_email(login)

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_access_and_refresh_token(
        self, user_data: UserLoginDTO
    ) -> AccessAndRefreshTokenDTO:
        try:
            user_result_data = await self.get_user_by_username_or_email(
                user_data.login
            )
        except UserDoesNotExistException as e:
            raise InvalidCredentialsException() from e
        if not user_result_data.is_active:
            raise UserIsNotActiveException()
        if not self.password_manager.verify_password(
            user_data.password, user_result_data.hashed_password
        ):
            raise WrongPasswordException()

        token_sub = str(user_result_data.id)
        return AccessAndRefreshTokenDTO(
            access_token=self.token_manager.create_token(
                sub=token_sub, token_type=TokenTypeEnum.ACCESS
            ),
            refresh_token=self.token_manager.create_token(
                sub=token_sub, token_type=TokenTypeEnum.REFRESH
            ),
        )

    async def get_user_by_token(
        self, token: str, token_type: TokenTypeEnum
    ) -> UserDTO:
        payload = self.token_manager.get_validated_token_data(
            token, token_type
        )
        result_user = await self.user_repository.get_user_by_id(
            int(payload.get("sub"))
        )
        if (
            payload.get("iat")
            < (
                result_user.password_updated_at - datetime.timedelta(seconds=1)
            ).timestamp()
        ):
            raise PasswordChangedException()
        return result_user

    async def get_new_access_token_by_refresh_token(
        self, token: str
    ) -> AccessTokenDTO:
        result_user = await self.get_user_by_token(
            token, TokenTypeEnum.REFRESH
        )
        access_token = self.token_manager.create_token(
            str(result_user.id), TokenTypeEnum.ACCESS
        )
        return AccessTokenDTO(access_token=access_token)

    async def update_user_password(
        self, user_id: int, password_data: PasswordChangeDTO
    ) -> None:
        user_data = await self.get_user_by_id(user_id)
        if not self.password_manager.verify_password(
            password_data.old_password, user_data.hashed_password
        ):
            raise WrongPasswordException()
        await self.user_repository.update_user_password(
            user_id,
            self.password_manager.hash_password(password_data.password),
        )
