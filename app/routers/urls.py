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
    except RedisError as e:
        cached_url = None
        print(f"Redis error: {e}")

    if cached_url:
        return RedirectResponse(
            url=cached_url,
            status_code=307,
            # Status code will be 307 by default, but explicitly setting it for clarity
        )

    url_record = db.query(Url).filter(Url.short_code == short_code).first()

    if not url_record:
        raise HTTPException(status_code=404, detail="Short URL not found")

    try:
        redis_client.set(
            f"url:{short_code}", url_record.original_url, ex=86400
        )  # Cache for 24 hours

    except RedisError as e:
        print(f"Redis error: {e}")

    return RedirectResponse(
        url=url_record.original_url,
        status_code=307,
        # Status code will be 307 by default, but explicitly setting it for clarity
    )
