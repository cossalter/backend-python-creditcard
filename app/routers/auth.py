import os
from datetime import timedelta
from typing import Annotated, TypeAlias

from fastapi import Depends, HTTPException, status


from sqlalchemy.orm import Session

from entities.user import User
from base.router import BaseAPIRouter

from database.models.user import get_user
from database.base import get_db

from jose import JWTError
from base.utils import verify_password
from auth.jwt import (
    Token,
    TokenData,
    create_access_token,
    get_data_from_token,
    oauth2_scheme,
)


router = BaseAPIRouter(prefix="/token", tags=["token"])


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.password):
        return False

    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = get_data_from_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


CurrentUser: TypeAlias = Annotated[User, Depends(get_current_active_user)]


@router.post("/", response_model=Token)
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "Bearer"}
