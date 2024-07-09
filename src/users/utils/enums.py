from enum import Enum


class UserEnum(Enum):
    USER_EXISTS = 'user exists'
    USER_CREATED = 'user created'
    USER_ALREADY_EXISTS = 'user already exists'
    WRONG_PASSWORD = 'wrong password'
    USER_NOT_EXISTS = 'user not exists'
    USER_IS_NOT_ACTIVE = 'user is not active'
    SUCCESS_LOGIN = 'success login'
    INVALID_TOKEN = 'invalid token'
    TOKEN_EXPIRED = 'token expired'
    TOKEN_IS_VALID = 'token is valid'
