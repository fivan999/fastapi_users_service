from src.domain.exceptions.base import AppException


class UserAlreadyExistsException(AppException):
    detail = "user already exists"
    status_code = 409


class UserDoesNotExistException(AppException):
    detail = "user does not exist"
    status_code = 404


class UserIsNotActiveException(AppException):
    detail = "user is not active"
    status_code = 401
