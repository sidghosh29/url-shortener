from pydantic import BaseModel, HttpUrl
from typing import Optional


class UrlRequest(BaseModel):
    url: HttpUrl


class UrlResponse(BaseModel):
    short_url: str
    short_code: str | None = None


class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class UserSignInRequest(BaseModel):
    username: str
    password: str


class UserSignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthenticatedUser(BaseModel):
    id: str
    email: str
    roles: list[str]
    first_name: str | None = None
    last_name: str | None = None
