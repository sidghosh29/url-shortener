import secrets

BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

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

def generate_random_base62_code(length: int = 10) -> str:
    return ''.join(secrets.choice(BASE62_ALPHABET) for _ in range(length))