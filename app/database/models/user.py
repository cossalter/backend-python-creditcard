from base.utils import get_password_hash
from database.base import BaseModel

from database.models.credit_card import CreditCardModel

from typing import TYPE_CHECKING, Self
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.orm.query import Query

if TYPE_CHECKING:
    from entities.user import User


class UserModel(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    cards: Mapped[list[CreditCardModel]] = relationship(
        foreign_keys=[CreditCardModel.user_id]
    )

    @classmethod
    def create(
        cls,
        db: Session,
        user: "User",
        password: str,
        *,
        commit: bool = True,
    ) -> Self:
        user_model = cls(
            username=user.username,
            is_active=user.is_active,
            password=get_password_hash(password),
        )

        return user_model.save(db, commit)


def get_user(
    db: Session,
    user: "User",
    *,
    query: Query[UserModel] = None,
) -> UserModel | None:
    if query is None:
        query = db.query(UserModel)

    return query.where(UserModel.username == user.username).first()
