from pydantic import BaseModel, HttpUrl


class UrlRequest(BaseModel):
    url: HttpUrl


class UrlResponse(BaseModel):
    short_url: str
    short_code: str | None = None
