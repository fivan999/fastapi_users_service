from pydantic import BaseModel


class UserIdDTO(BaseModel):
    id: int


class HttpErrorDTO(BaseModel):
    detail: str
