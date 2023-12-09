import os
import datetime

from typing import Any
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


def _encode(data: Any) -> str:
    return jwt.encode(
        data, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM")
    )


def get_data_from_token(token) -> dict[str, Any]:
    return jwt.decode(
        token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")]
    )


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})

    return _encode(to_encode)
