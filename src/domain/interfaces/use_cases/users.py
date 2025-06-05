from abc import ABC, abstractmethod

from src.domain.dtos.password import PasswordChangeDTO
from src.domain.dtos.tokens import AccessAndRefreshTokenDTO, AccessTokenDTO
from src.domain.dtos.users import UserCreateDTO, UserDTO, UserLoginDTO
from src.domain.enums import TokenTypeEnum


class IUserUseCase(ABC):
    @abstractmethod
    def create_user(self, user_data: UserCreateDTO) -> UserDTO:
        pass

    @abstractmethod
    def get_user_by_username_or_email(self, login: str) -> UserDTO:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserDTO:
        pass

    @abstractmethod
    def get_access_and_refresh_token(
        self, user_data: UserLoginDTO
    ) -> AccessAndRefreshTokenDTO:
        pass

    @abstractmethod
    def get_new_access_token_by_refresh_token(
        self, token: str
    ) -> AccessTokenDTO:
        pass

    @abstractmethod
    def update_user_password(
        self, user_id: int, password_data: PasswordChangeDTO
    ) -> None:
        pass
