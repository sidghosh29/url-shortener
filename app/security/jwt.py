from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


def create_jwt_token(user_id: int):
    iat = datetime.now(timezone.utc)
    expire = iat + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "iat": iat,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_jwt_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.InvalidTokenError:
        raise ValueError("Invalid or expired token") from None
