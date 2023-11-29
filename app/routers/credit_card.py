from fastapi import Depends, status, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from base.router import BaseAPIRouter

from entities.factories.credit_card import CreditCardFactory
from entities.credit_card import CreditCard

from database.base import get_db
from database.models.credit_card import create_credit_card, get_cards, get_card

from routers.auth import CurrentUser

router = BaseAPIRouter(prefix="/credit-card", tags=["credit-card"])


def serializer(creditcard: CreditCard) -> dict:
    return {
        **creditcard.to_dict(),
        "exp_date": creditcard.exp_date.strftime("%m/%Y"),
        "brand": creditcard.brand,
    }


# POST


class CreateCardInput(BaseModel):
    exp_date: str = Field(
        title="Expiration data",
        min_length=7,
        max_length=7,
        pattern="[0-1][0-9]/[0-9]{4}",
    )
    holder: str = Field(title="Name of card owner", min_length=2)
    number: str = Field(title="Card number", min_length=16, max_length=16)
    cvv: int | None = Field(title="Security code", ge=100, le=9999, default=None)


@router.post("/")
async def create(
    input: CreateCardInput,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    try:
        card = CreditCardFactory.create(**input.model_dump())

        if any([c for c in get_cards(db, current_user.id) if card.number == c.number]):
            raise ValueError("Card number already registered!")

        create_credit_card(db, card, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return serializer(card)


@router.get("/")
async def cards(current_user: CurrentUser, db: Session = Depends(get_db)):
    return [serializer(card) for card in get_cards(db, current_user.id)]


@router.get("/{card_id}")
async def card(card_id: int, current_user: CurrentUser, db: Session = Depends(get_db)):
    if card := get_card(db, current_user.id, card_id):
        return serializer(card)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="There is no registration for this card",
    )
