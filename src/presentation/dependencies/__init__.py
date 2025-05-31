from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.db.dependencies import DbProvider
from src.presentation.dependencies.credentials import CredentialsProvider
from src.presentation.dependencies.repositories.users import (
    UserRepositoryProvider,
)
from src.presentation.dependencies.security.password import (
    PasswordManagerProvider,
)
from src.presentation.dependencies.security.tokens import (
    JwtTokenManagerProvider,
)
from src.presentation.dependencies.use_cases.users import UserUseCaseProvider


def create_async_container() -> AsyncContainer:
    container = make_async_container(
        CredentialsProvider(),
        DbProvider(),
        UserRepositoryProvider(),
        UserUseCaseProvider(),
        FastapiProvider(),
        PasswordManagerProvider(),
        JwtTokenManagerProvider(),
    )
    return container
