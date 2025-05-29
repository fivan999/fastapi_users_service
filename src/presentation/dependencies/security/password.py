from dishka import Provider, Scope, provide

from src.application.services.password_manager import BcryptPasswordManager
from src.domain.interfaces.password_manager import IPasswordManager


class PasswordManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_password_manager(self) -> IPasswordManager:
        return BcryptPasswordManager()
