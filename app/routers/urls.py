import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from redis.exceptions import RedisError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.rate_limit import rate_limit
from app.models import Url
from app.redis_client import redis_client
from app.schemas import UrlRequest, UrlResponse
from app.services.url_service import UrlService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/shorten",
    status_code=201,
    response_model=UrlResponse,
    dependencies=[Depends(rate_limit)],
)
def shorten_url(request: UrlRequest, db: Session = Depends(get_db)):
    service = UrlService(db)
    try:
        return service.create_short_url(request)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Could not create short URL"
        ) from None


@router.get("/{short_code}", status_code=307)
def redirect_to_original_url(short_code: str, db: Session = Depends(get_db)):
    try:
        cached_url = redis_client.get(f"url:{short_code}")
    except RedisError:
        logger.warning(
            "Redis lookup failed for short code %s; falling back to database",
            short_code,
            exc_info=True,
        )
        cached_url = None

    if cached_url:
        logger.debug("Redirect cache hit for short code %s", short_code)
        return RedirectResponse(
            url=cached_url,
            status_code=307,
            # Status code will be 307 by default, but explicitly setting it for clarity
        )

    url_record = db.query(Url).filter(Url.short_code == short_code).first()

    if not url_record:
        logger.info("Redirect requested for unknown short code %s", short_code)
        raise HTTPException(status_code=404, detail="Short URL not found")

    try:
        redis_client.set(
            f"url:{short_code}", url_record.original_url, ex=86400
        )  # Cache for 24 hours

    except RedisError:
        logger.warning(
            "Redis cache write failed for short code %s", short_code, exc_info=True
        )

    logger.debug("Redirect cache miss for short code %s", short_code)

    return RedirectResponse(
        url=url_record.original_url,
        status_code=307,
        # Status code will be 307 by default, but explicitly setting it for clarity
    )
