from passlib.context import CryptContext

from src.domain.interfaces.password_manager import IPasswordManager


class BcryptPasswordManager(IPasswordManager):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
