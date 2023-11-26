from pydantic import BaseModel, Field

from base.router import BaseAPIRouter

router = BaseAPIRouter(prefix="/credit-card", tags=["credit-card"])

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
    return input
