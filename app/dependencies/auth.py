from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

bearer_scheme = HTTPBearer(auto_error=False)


def ensure_bearer(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    # Do nothing - this is just to make Swagger show the lock button
    return


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = getattr(request.state, "user_id", None)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    return user


def require_roles(*required_roles: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return checker
