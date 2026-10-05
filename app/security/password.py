# app/security/password.py
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended() 
# Use the recommended password hashing algorithm (currently Argon2)

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)