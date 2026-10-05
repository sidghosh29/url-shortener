import logging

from app.constants import MAX_CODE_GENERATION_ATTEMPTS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Url
from app.schemas import UrlRequest, UrlResponse
from app.utils import generate_random_base62_code

logger = logging.getLogger(__name__)


class UrlService:
    def __init__(self, db: Session):
        self.db = db

    def create_short_url(self, request: UrlRequest) -> UrlResponse:

        for _ in range(MAX_CODE_GENERATION_ATTEMPTS):
            try:
                url = Url(original_url=str(request.url))
                short_code = generate_random_base62_code()
                url.short_code = short_code
                self.db.add(url)
                # self.db.flush()  # Flush to get the auto-generated ID. Not required now. 
                self.db.commit()
                logger.info("Created short URL with code %s", url.short_code)

                return UrlResponse(
                    short_url=f"{settings.BASE_URL}/{url.short_code}",
                    short_code=url.short_code,
                )
            except IntegrityError as exc:
                self.db.rollback()
                diag = getattr(exc.orig, "diag", None)
                if diag and diag.constraint_name == "ix_urls_short_code":
                    logger.warning(f"Short code collision for {short_code}")
                    continue  # Try generating a new short code
                raise  # Re-raise other integrity errors


        raise RuntimeError("Unable to generate a unique short code")
