# app/security/password.py
import logging

from pwdlib import PasswordHash

logger = logging.getLogger(__name__)

password_hash = PasswordHash.recommended()
# Use the recommended password hashing algorithm (currently Argon2)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# DUMMY_HASHED_PASSWORD = hash_password("dummy_password")
DUMMY_HASHED_PASSWORD = "$argon2id$v=19$m=65536,t=3,p=4$I3Uc1jK3miC0ZnZBFrXf7A$CTweZ39EdGuGZIjrY2nvRvQqBOR8qH4GnqLp0C0ik20"  # noqa
