from pydantic import BaseModel


class AccessTokenDTO(BaseModel):
    access_token: str


class AccessAndRefreshTokenDTO(AccessTokenDTO):
    refresh_token: str
