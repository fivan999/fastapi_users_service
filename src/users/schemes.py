from pydantic import BaseModel, EmailStr


class UserBaseScheme(BaseModel):
    username: str
    email: EmailStr


class UserCreateScheme(UserBaseScheme):
    password: str


class UserShowScheme(UserBaseScheme):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserFullScheme(UserShowScheme):
    hashed_password: str

    class Config:
        orm_mode = True


class UserLoginScheme(BaseModel):
    login: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class AccessAndRefreshToken(AccessToken):
    refresh_token: str
