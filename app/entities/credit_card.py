import calendar
import datetime
import re

from dataclasses import dataclass

from base.entity import BaseEntity

from creditcard import CreditCard as NumberInfo

from typing import Self

DATE_FORMAT = "[0-1][0-9]/[0-9]{4}"


def get_last_day(month: int, year: int) -> int:
    return calendar.monthrange(year, month)[1]


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
        if self.exp_date <= today:
            raise ValueError("Expiration date must be a future date!")

        # the day in expiration date must be the last one in the month
        if self.exp_date.day != get_last_day(self.exp_date.month, self.exp_date.year):
            raise ValueError(
                "The day in expiration date must be the last one in the month!"
            )

        if not NumberInfo(self.number).is_valid():
            raise ValueError("The card number isn't valid!")

    @classmethod
    def get_month_year_from_str_exp_date(cls, exp_date: str) -> tuple[int, int]:
        if not re.fullmatch(DATE_FORMAT, exp_date):
            raise ValueError(
                "The exp_date parameter must be in the following format %m/%Y"
            )

        return map(int, exp_date.split("/", maxsplit=1))

    @classmethod
    def create(
        cls,
        exp_date: str | datetime.date,
        holder: str,
        number: str,
        cvv: int | None = None,
    ) -> Self:
        if isinstance(exp_date, str):
            month, year = cls.get_month_year_from_str_exp_date(exp_date)
            exp_date = datetime.date(year, month, get_last_day(month, year))

        return cls(exp_date, holder, number, cvv)
