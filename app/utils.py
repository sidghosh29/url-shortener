import secrets

from app.constants import BASE62_ALPHABET, SHORT_CODE_LENGTH


def encode_base62(num: int) -> str:
    if num < 0:
        raise ValueError("num must be non-negative")

    if 0 <= num <= 61:
        return BASE62_ALPHABET[num]
    encoded = ""

    while num > 0:
        remainder = num % 62
        num //= 62
        encoded = BASE62_ALPHABET[remainder] + encoded

    return encoded


def generate_random_base62_code(length: int = SHORT_CODE_LENGTH) -> str:
    return "".join(secrets.choice(BASE62_ALPHABET) for _ in range(length))
    # return "5LfLUoXZqM"  # For testing purposes, return a fixed code
