from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.dependencies.credentials import CredentialsProvider
from src.dependencies.db import DbProvider
from src.dependencies.repositories.users import UserRepositoryProvider
from src.dependencies.security.password import PasswordManagerProvider
from src.dependencies.security.tokens import JwtTokenManagerProvider
from src.dependencies.use_cases.users import UserUseCaseProvider


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
