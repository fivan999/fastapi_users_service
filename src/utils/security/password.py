from passlib.context import CryptContext


class PasswordManager:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Getting hashed value of a password

        Args:
            password (str)

        Returns:
            str: hashed passsword
        """
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(
        cls, plain_password: str, hashed_password: str
    ) -> bool:
        """
        Comparing password and hashed password

        Args:
            password (str)
            hashed_password (str)

        Returns:
            bool: are passwords equal
        """
        return cls.pwd_context.verify(plain_password, hashed_password)
