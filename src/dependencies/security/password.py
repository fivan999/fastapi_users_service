from dishka import Provider, Scope, provide

from src.utils.security.password import PasswordManager


class PasswordManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_password_manager(self) -> PasswordManager:
        return PasswordManager()
