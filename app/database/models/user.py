from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from database.base import Base
from database.models.credit_card import CreditCard

if TYPE_CHECKING:
    from entities.user import User as UserEntity


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    cards = relationship("CreditCard", foreign_keys=[CreditCard.user_id])


def _model2entity(user_model: CreditCard) -> "UserEntity":
    from entities.user import User as UserEntity

    user = UserEntity(
        username=user_model.username,
        password=user_model.password,
        is_active=user_model.is_active,
    )

    user.set_id(user_model.id)

    return user


def get_user(db: Session, username: str) -> "UserEntity | None":
    db_user = db.query(User).where(User.username == username).first()

    if db_user:
        return _model2entity(db_user)


def create_user(db: Session, user: "UserEntity") -> "UserEntity":
    from base.utils import get_password_hash

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return _model2entity(db_user)
