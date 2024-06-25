import secrets
import string
from typing import Union
from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher

ph = PasswordHasher()

API_KEY_PREFIX = "gpustack"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_hashed_secret(hashed: str | bytes, plain: str | bytes) -> bool:
    try:
        return ph.verify(hashed, plain)
    except Exception:
        return False


def get_secret_hash(plain: str | bytes):
    return ph.hash(plain)


def create_access_token(username: str, expires_delta: Union[timedelta, None] = None):
    to_encode = {"sub": username}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def generate_secure_password(length=12):
    if length < 8:
        raise ValueError("Password length should be at least 8 characters")

    special_characters = "!@#$%^&*_+"
    characters = string.ascii_letters + string.digits + special_characters
    while True:
        password = ''.join(secrets.choice(characters) for i in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in special_characters for c in password)
        ):
            return password
