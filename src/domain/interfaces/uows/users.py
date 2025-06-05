from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from src.domain.interfaces.repositories.users import IUserRepository


class IUserUnitOfWork(ABC):
    users: IUserRepository

    @asynccontextmanager
    @abstractmethod
    async def start(self):
        pass
