from pydantic import BaseModel, EmailStr


class UserBaseScheme(BaseModel):
    username: str
    email: EmailStr


class UserCreateScheme(UserBaseScheme):
    password: str


class UserScheme(UserBaseScheme):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
