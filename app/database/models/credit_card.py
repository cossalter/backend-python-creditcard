import datetime
from base.utils import encrypt, decrypt

from database.base import BaseModel

from typing import Self

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import Mapped, Session, mapped_column

from entities.user import User
from entities.credit_card import CreditCard


class CreditCardModel(BaseModel):
    __tablename__ = "credit_cards"

    holder: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=False, index=True)
    exp_date: Mapped[datetime.date] = mapped_column(nullable=False)
    cvv: Mapped[int] = mapped_column(nullable=True)

    user_id = Column("user_id", ForeignKey("users.id"), nullable=True)

    @classmethod
    def create(
        cls,
        db: Session,
        card: CreditCard,
        *,
        user: User | None = None,
        commit: bool = True,
    ) -> Self:
        card_model = cls(
            exp_date=card.exp_date,
            holder=card.holder,
            number=encrypt(card.number),
            cvv=card.cvv,
            user_id=user and user.id,
        )

        return card_model.save(db, commit)

    def to_entinty(self) -> CreditCard:
        return CreditCard(
            exp_date=self.exp_date,
            holder=self.holder,
            number=decrypt(self.number),
            cvv=self.cvv,
        )
