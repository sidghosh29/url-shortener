import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Role, User
from app.schemas import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserSignInRequest,
    UserSignInResponse,
)
from app.security.jwt import create_jwt_token
from app.security.password import DUMMY_HASHED_PASSWORD, hash_password, verify_password

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", status_code=201)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    email = request.email
    username = request.username
    password = request.password

    member_role = db.execute(select(Role).where(Role.name == "member")).scalar_one()

    # Create the new user
    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role_id=member_role.id,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserRegisterResponse(
            username=new_user.username, email=new_user.email, role=new_user.role.name
        )
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
            ) from None

        logger.exception("Database constraint failed during user registration")
        raise


@router.post("/signin", response_model=UserSignInResponse, status_code=200)
def signin(request: UserSignInRequest, db: Session = Depends(get_db)):
    username = request.username
    password = request.password

    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        verify_password(
            password, DUMMY_HASHED_PASSWORD
        )  # Dummy verification to mitigate timing attacks
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_jwt_token(user.id)

    return UserSignInResponse(access_token=access_token)
