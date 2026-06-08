from fastapi import HTTPException, Request

from app.rate_limiters.fixed_window import fixed_window_limiter


def rate_limit(request: Request):
    client_ip = request.client.host
    print(f"Client IP: {client_ip}")
    key = f"rate_limit:shorten:{client_ip}"
    if not fixed_window_limiter.allow_request(key):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )