from abc import ABC, abstractmethod

from src.domain.enums import TokenTypeEnum


class ITokenManager(ABC):
    @abstractmethod
    def create_token(self, sub: str, token_type: TokenTypeEnum) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        pass

    @abstractmethod
    def get_validated_token_data(
        cls, token: str, expected_token_type: TokenTypeEnum
    ) -> dict:
        pass
