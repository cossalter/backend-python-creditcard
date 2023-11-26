from fastapi import status, HTTPException
from pydantic import BaseModel, Field

from base.router import BaseAPIRouter
from credit_card.factory import CreditCardFactory
from credit_card.entity import CreditCard

router = BaseAPIRouter(prefix="/credit-card", tags=["credit-card"])


def serializer(creditcard: CreditCard) -> dict:
    return {
        **creditcard.to_dict(),
        "exp_date": creditcard.exp_date.strftime("%m/%Y"),
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
async def create(input: CreateCardInput):
    try:
        card = CreditCardFactory.create(**input.model_dump())

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return serializer(card)
