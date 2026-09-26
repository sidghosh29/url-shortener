import logging

from fastapi import HTTPException, Request

# from app.rate_limiters.fixed_window import fixed_window_limiter
from app.rate_limiters.token_bucket import token_bucket_limiter

logger = logging.getLogger(__name__)


def rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:shorten:{client_ip}"
    # if not fixed_window_limiter.allow_request(key):
    if not token_bucket_limiter.allow_request(key):
        logger.warning("Rate limit exceeded for request")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
