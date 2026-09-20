from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Url
from app.schemas import UrlRequest, UrlResponse
from app.utils import encode_base62
from app.config import settings


class UrlService:
    def __init__(self, db: Session):
        self.db = db

    def create_short_url(self, request: UrlRequest) -> UrlResponse:
        try:
            url = Url(original_url=str(request.url))

            self.db.add(url)
            self.db.flush()  # Flush to get the auto-generated ID
            url.short_code = encode_base62(url.id)
            self.db.commit()

            return UrlResponse(
                short_url=f"{settings.BASE_URL}/{url.short_code}",
                short_code=url.short_code,
            )
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            self.db.rollback()
            raise
