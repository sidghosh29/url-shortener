from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, get_db
from app.models import Base, Url
from app.schemas import UrlRequest, UrlResponse

from app.utils import generate_random_base62_code, encode_base62
from app.config import settings
from app.redis_client import redis_client
from redis.exceptions import RedisError


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "URL Shortener API"}


@app.post("/shorten", status_code=201, response_model=UrlResponse)
def shorten_url(
    request: UrlRequest,
    db: Session = Depends(get_db)
):
    try:

        url = Url(
            original_url=str(request.url)
        )

        db.add(url)
        db.flush()  # Flush to get the auto-generated ID
        url.short_code = encode_base62(url.id)
        db.commit()

        return UrlResponse(short_url=f"{settings.BASE_URL}/{url.short_code}", short_code=url.short_code)
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        db.rollback()
        raise HTTPException(status_code=409, detail="Could not create short URL")
    # while True:

    #     try:

    #         url = Url(
    #             short_code=generate_random_base62_code(),
    #             original_url=str(request.url)
    #         )

    #         db.add(url)
    #         db.commit()

    #         return {"message": "saved"}
    #     except IntegrityError:
    #         db.rollback()
    #         return {"message": "short code collision, try again"}


@app.get("/{short_code}", status_code=307)
def redirect_to_original_url(short_code: str, db: Session = Depends(get_db)):

    try:
        cached_url = redis_client.get(f"url:{short_code}")
    except RedisError as e:
        cached_url = None
        print(f"Redis error: {e}")

    if cached_url:
        return RedirectResponse(
            url=cached_url,
            status_code=307 
            # Status code will be 307 by default, but explicitly setting it for clarity
        )

    url_record = (
        db.query(Url)
        .filter(Url.short_code == short_code)
        .first()
    )

    if not url_record:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )
    
    try:
    
        redis_client.set(f"url:{short_code}", url_record.original_url, ex=86400)  # Cache for 24 hours

    except RedisError as e:
        print(f"Redis error: {e}")

    return RedirectResponse(
        url=url_record.original_url,
        status_code=307 
        # Status code will be 307 by default, but explicitly setting it for clarity
    )