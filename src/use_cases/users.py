import datetime

from src.repositories.users import UserRepository
from src.schemes.password import PasswordChangeScheme
from src.schemes.tokens import AccessAndRefreshToken, AccessToken
from src.schemes.users import (
    UserCreateScheme,
    UserFullScheme,
    UserLoginScheme,
    UserShowScheme,
)
from src.utils.enums import UserEnum
from src.utils.password import get_hashed_password, verify_password
from src.utils.tokens import (
    create_access_or_refresh_token,
    get_validated_token_data,
)


class UserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(
        self, user_data: UserCreateScheme
    ) -> tuple[UserEnum, UserShowScheme | None]:
        """
        Creating a user with user's data

        Args:
            user_data (UserCreateScheme): user's data

        Returns:
            tuple[
                UserEnum, UserShowScheme | None
            ]: Enum with creating status and data
        """
        user_data.password = get_hashed_password(user_data.password)
        return await self.user_repository.create_user(user_data)

    async def get_user_by_username_or_email(
        self, login: str
    ) -> tuple[UserEnum, UserFullScheme]:
        """
        Getting a user by username or email

        Args:
            login (str): username or email

        Returns:
            tuple[UserEnum, UserFullScheme]: Enum with status and user's data
        """
        user_get_status, user_result_data = (
            await self.user_repository.get_user_by_username_or_email(login)
        )
        if user_get_status == UserEnum.USER_NOT_EXISTS:
            return UserEnum.USER_NOT_EXISTS, None
        if not user_result_data.is_active:
            return UserEnum.USER_IS_NOT_ACTIVE, None
        return UserEnum.USER_EXISTS, UserFullScheme(
            **user_result_data.__dict__
        )

    async def get_access_and_refresh_token(
        self, user_data: UserLoginScheme
    ) -> tuple[UserEnum, AccessAndRefreshToken | None]:
        """
        Creating access and refresh token for user

        Args:
            user_data (UserLoginScheme): user's data

        Returns:
            tuple[
                UserEnum, AccessAndRefreshToken | None
            ]: Enum with creating status and tokens
        """
        user_get_status, user_result_data = (
            await self.get_user_by_username_or_email(user_data.login)
        )
        if user_get_status != UserEnum.USER_EXISTS:
            return user_get_status, None
        if not verify_password(
            user_data.password, user_result_data.hashed_password
        ):
            return UserEnum.WRONG_PASSWORD, None

        token_sub = user_result_data.username
        return UserEnum.SUCCESS_LOGIN, AccessAndRefreshToken(
            access_token=create_access_or_refresh_token(
                sub=token_sub, token_type='access_token'
            ),
            refresh_token=create_access_or_refresh_token(
                sub=token_sub, token_type='refresh_token'
            ),
        )

    async def get_user_by_token(
        self, token: str, token_type: str
    ) -> tuple[UserEnum, UserFullScheme | None]:
        """
        Getting user's data by jwt token

        Args:
            token (str): jwt token
            token_type (str): type of a token (access or refresh)

        Returns:
            tuple[
                UserEnum, UserFullScheme | None
            ]: Enum with getting status and user's data
        """
        token_status, payload = get_validated_token_data(token, token_type)
        if token_status != UserEnum.TOKEN_IS_VALID:
            return token_status, None
        result_status, result_user = (
            await self.user_repository.get_user_by_username_or_email(
                payload.get('sub')
            )
        )
        if result_status == UserEnum.USER_NOT_EXISTS:
            return UserEnum.USER_NOT_EXISTS, None
        if payload.get('iat') < (result_user.password_updated_at - datetime.timedelta(seconds=1)).timestamp():
            return UserEnum.PASSWORD_CHANGED, None
        return UserEnum.USER_EXISTS, UserFullScheme(**result_user.__dict__)

    async def get_new_access_token_by_refresh_token(
        self, token: str
    ) -> tuple[UserEnum, AccessToken | None]:
        """
        Getting a new access token by resresh token

        Args:
            token (str): refresh token

        Returns:
            tuple[
                UserEnum, AccessToken | None
            ]: Enum with getting status and access token
        """
        result_status, result_user = await self.get_user_by_token(
            token, 'refresh_token'
        )
        if result_status != UserEnum.USER_EXISTS:
            return result_status, None
        access_token = create_access_or_refresh_token(
            result_user.username, 'access_token'
        )
        return UserEnum.TOKEN_IS_VALID, AccessToken(access_token=access_token)

    async def update_user_password(
        self, user_data: UserFullScheme, password_data: PasswordChangeScheme
    ) -> UserEnum:
        """
        Update password of a user

        Args:
            user_data (UserFullScheme): user's data
            password_data (
                PasswordChangeScheme
            ): dto with old and new passwords

        Returns:
            UserEnum: status of updating a password
        """
        if not verify_password(
            password_data.old_password, user_data.hashed_password
        ):
            return UserEnum.WRONG_PASSWORD
        result_status = await self.user_repository.update_user_password(
            user_data.username, get_hashed_password(password_data.password)
        )
        return result_status
