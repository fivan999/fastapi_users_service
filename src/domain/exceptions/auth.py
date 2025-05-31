from src.domain.exceptions.base import AppException


class WrongPasswordException(AppException):
    detail = "wrong password"
    status_code = 401


class PasswordChangedException(AppException):
    detail = "password was changed"
    status_code = 401


class InvalidCredentialsException(AppException):
    detail = "invalid login or password"
    status_code = 401
