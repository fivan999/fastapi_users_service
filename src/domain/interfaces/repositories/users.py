from abc import ABC, abstractmethod

from src.domain.dtos.users import UserCreateDTO, UserDTO


class IUserRepository(ABC):
    @abstractmethod
    def add(self, user_data: UserCreateDTO) -> UserDTO:
        pass

    @abstractmethod
    def get_user_by_username_or_email(self, login: str) -> UserDTO:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserDTO:
        pass

    @abstractmethod
    def update_user_password(self, user_id: int, new_password: str) -> None:
        pass
