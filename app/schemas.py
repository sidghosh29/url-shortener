from pydantic import BaseModel, HttpUrl


class UrlRequest(BaseModel):
    url: HttpUrl


class UrlResponse(BaseModel):
    short_url: str
    short_code: str | None = None


class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class UserRegisterResponse(BaseModel):
    username: str
    email: str
    role: str


class UserSignInRequest(BaseModel):
    username: str
    password: str


class UserSignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
