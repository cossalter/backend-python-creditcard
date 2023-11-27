from base.router import BaseAPIRouter

from user.entity import User
from routers.auth import CurrentUser


router = BaseAPIRouter(prefix="/users", tags=["user"])


@router.get("/me", response_model=User)
async def me(current_user: CurrentUser):
    return current_user
