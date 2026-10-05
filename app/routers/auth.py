import logging

from fastapi import APIRouter, Depends, HTTPException
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.models import User
from app.redis_client import redis_client
from app.schemas import UserRegisterRequest
from app.security import hash_password, verify_password

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("register", status_code=201)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    email = request.email
    username = request.username
    password = request.password

    # Create the new user
    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as exc:
        db.rollback()

        diag = getattr(exc.orig, "diag", None)
        if diag and diag.constraint_name in {
            "ix_users_username",
            "ix_users_email",
        }:
            raise HTTPException(
                status_code=409,
                detail="Unable to create account with the provided information.",
            )

        logger.exception("Database constraint failed during user registration")
        raise