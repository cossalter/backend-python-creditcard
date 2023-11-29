import datetime
import calendar

from entities.credit_card import CreditCard


class CreditCardFactory:
    @classmethod
    def create(
        cls,
        exp_date: str | datetime.date,
        holder: str,
        number: str,
        cvv: int | None = None,
    ) -> CreditCard:
        if isinstance(exp_date, str):
            month, year = map(int, exp_date.split("/"))
            last_day = calendar.monthrange(year, month)[1]

            exp_date = datetime.date(year, month, last_day)

        return CreditCard(exp_date, holder, number, cvv)
