import datetime

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import Mapped, Session, mapped_column

from database.base import Base
from base.utils import base64_decode, base64_encode

if TYPE_CHECKING:
    from entities.credit_card import CreditCard as CreditCardEntity


class CreditCard(Base):
    __tablename__ = "credit_cards"

    holder: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=False, index=True)
    exp_date: Mapped[datetime.date] = mapped_column(nullable=False)
    cvv: Mapped[int] = mapped_column(nullable=True)

    user_id = Column("user_id", ForeignKey("users.id"), nullable=True)


def _model2entity(card_model: CreditCard) -> "CreditCardEntity":
    from app.entities.credit_card import CreditCard as CreditCardEntity

    card = CreditCardEntity(
        exp_date=card_model.exp_date,
        holder=card_model.holder,
        number=base64_decode(card_model.number),
        cvv=card_model.cvv,
    )

    card.set_id(card_model.id)

    return card


def get_card(db: Session, user_id: int, card_id: int) -> "CreditCardEntity | None":
    from database.models.user import User

    card = (
        db.query(CreditCard).where(CreditCard.id == card_id, User.id == user_id).first()
    )

    if card:
        return _model2entity(card)


def get_cards(db: Session, user_id: int) -> list["CreditCardEntity"]:
    from database.models.user import User

    user = db.query(User).where(User.id == user_id).first()

    return [_model2entity(card) for card in user.cards]


def create_credit_card(
    db: Session,
    card: "CreditCardEntity",
    user_id: int,
) -> "CreditCardEntity":
    db_card = CreditCard(
        exp_date=card.exp_date,
        holder=card.holder,
        number=base64_encode(card.number),
        cvv=card.cvv,
        user_id=user_id,
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)

    return _model2entity(db_card)
