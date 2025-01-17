from enum import Enum


class UserEnum(Enum):
    USER_EXISTS = 'user exists'
    USER_CREATED = 'user created'
    USER_ALREADY_EXISTS = 'user already exists'
    USER_NOT_EXISTS = 'user not exists'
    USER_IS_NOT_ACTIVE = 'user is not active'


class TokenEnum(Enum):
    INVALID_TOKEN = 'invalid token'
    TOKEN_EXPIRED = 'token expired'
    TOKEN_IS_VALID = 'token is valid'


class TokenTypeEnum(Enum):
    ACCESS = 0
    REFRESH = 1


class AuthEnum(Enum):
    SUCCESS_LOGIN = 'success login'
    PASSWORD_CHANGED = 'password changed'
    WRONG_PASSWORD = 'wrong password'
