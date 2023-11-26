import datetime

from dataclasses import dataclass

from base.entity import BaseEntity

from creditcard import CreditCard as NumberInfo


@dataclass
class CreditCard(BaseEntity):
    exp_date: datetime.date
    holder: str
    number: str
    cvv: int | None = None

    @property
    def brand(self) -> str:
        return NumberInfo(self.number).get_brand()

    def validation(self) -> None:
        today = datetime.date.today()

        # expiration date must be in the future
        if self.exp_date.year < today.year or (
            self.exp_date.year == today.year and self.exp_date.month < today.month
        ):
            raise ValueError("Expiration date must be a future date!")

        if not NumberInfo(self.number).is_valid():
            raise ValueError("The card number isn't valid!")
