import secrets
from datetime import datetime, timedelta
from typing import Final, Optional

from jose import jwt
from passlib.context import CryptContext

from backend.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
EMAIL_RESET_TOKEN_EXPIRE_HOURS: Final = 1
PASSWORD_REST_TOKEN_EXPIRY: Final = 60
settings = get_settings()
SECRET_KEY = settings.SECRET_KEY


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def generate_salt() -> str:
    return secrets.token_hex(16)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def generate_password_reset_token(email: str) -> str:
    access_token_expires = timedelta(minutes=PASSWORD_REST_TOKEN_EXPIRY)
    encoded_jwt = create_access_token(
        data={"email": email}, expires_delta=access_token_expires
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
