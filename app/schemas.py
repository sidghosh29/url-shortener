from pydantic import BaseModel, HttpUrl
from typing import Optional

class UrlRequest(BaseModel):
    url: HttpUrl

class UrlResponse(BaseModel):
    short_url: str
    short_code: Optional[str] = None