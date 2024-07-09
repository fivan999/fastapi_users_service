from src.users.repositories import UserRepository
from src.users.schemes import UserCreateScheme, UserShowScheme, UserLoginScheme, AccessAndRefreshToken, UserFullScheme, AccessToken
from src.users.utils.enums import UserEnum
from src.users.utils.password import get_hashed_password, verify_password
from src.users.utils.tokens import create_access_or_refresh_token, get_validated_token_data
from jwt import ExpiredSignatureError


class UserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(
        self, user_data: UserCreateScheme
    ) -> tuple[UserEnum, UserShowScheme | None]:
        user_data.password = get_hashed_password(user_data.password)
        return await self.user_repository.create_user(user_data)

    async def user_login(
        self, user_data: UserLoginScheme
    ) -> tuple[UserEnum, AccessAndRefreshToken | None]:
        user_get_status, user_result_data = (
            await self.user_repository.get_user_by_username_or_email(
                user_data.login
            )
        )
        if user_get_status == UserEnum.USER_NOT_EXISTS:
            return UserEnum.USER_NOT_EXISTS, None
        if not user_result_data.is_active:
            return UserEnum.USER_IS_NOT_ACTIVE, None
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

    async def get_user_by_access_token(
        self, token: str
    ) -> tuple[UserEnum, UserFullScheme | None]:
        token_status, payload = get_validated_token_data(token, 'access_token')
        if token_status != UserEnum.TOKEN_IS_VALID:
            return token_status, None
        result_status, result_user = (
            await self.user_repository.get_user_by_username_or_email(
                payload.get('sub')
            )
        )
        if result_status == UserEnum.USER_NOT_EXISTS:
            return UserEnum.USER_NOT_EXISTS, None
        return UserEnum.USER_EXISTS, UserFullScheme(**result_user.__dict__)

    async def get_new_access_token_by_refresh_token(
        self, token: str
    ) -> tuple[UserEnum, AccessToken | None]:
        token_status, payload = get_validated_token_data(token, 'refresh_token')
        if token_status != UserEnum.TOKEN_IS_VALID:
            return token_status, None
        result_status, result_user = (
            await self.user_repository.get_user_by_username_or_email(
                payload.get('sub')
            )
        )
        if result_status == UserEnum.USER_NOT_EXISTS:
            return UserEnum.USER_NOT_EXISTS, None
        access_token = create_access_or_refresh_token(
            result_user.username, 'access_token'
        )
        return UserEnum.TOKEN_IS_VALID, AccessToken(access_token=access_token)
