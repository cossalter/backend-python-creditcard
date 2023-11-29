from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from entities.user import User
from routers.auth import CurrentUser
from base.router import BaseAPIRouter

from database.base import get_db
from database.user.model import create_user, get_user


router = BaseAPIRouter(prefix="/users", tags=["user"])


class CreateUserInput(BaseModel):
    username: str = Field(title="Name used to login")
    password: str = Field(title="Your password")
    confirm_password: str = Field(title="Confirme your password")


@router.post("/")
async def create(input: CreateUserInput, db: Session = Depends(get_db)):
    user = User(username=input.username, password=input.password, is_active=True)

    if not user.confirm_password(input.confirm_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The passwords field isn't the same",
        )

    if get_user(db, input.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'The "{input.username}" username already exists!',
        )

    return create_user(db, user).to_dict()


@router.get("/me", response_model=User)
async def me(current_user: CurrentUser):
    return current_user
