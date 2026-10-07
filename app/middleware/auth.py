import logging

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.security.jwt import decode_jwt_token

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.removeprefix("Bearer ").strip()

            try:
                payload = decode_jwt_token(token)
                user_id = int(payload.get("sub"))
                request.state.user_id = user_id

            except ValueError as e:
                logger.error(f"JWT decoding error: {e}")
                raise HTTPException(
                    status_code=401, detail="Invalid or expired token"
                ) from None

        return await call_next(request)
