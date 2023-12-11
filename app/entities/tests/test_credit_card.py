"""
All the fake data like number, exp_date and cvv to create the credit card tests,
was generate by https://www.4devs.com.br/gerador_de_numero_cartao_credito
"""

import pytest
import datetime
from freezegun import freeze_time

from entities.credit_card import CreditCard


class TestCreditCard:
    @freeze_time("2023-11-26")
    def test_create_credit_card(self):
        creditcard_aura = CreditCard(
            exp_date=datetime.date(2024, 5, 31),
            holder="Fulano Silva",
            number="5006114021788551",
        )

        assert creditcard_aura.exp_date == datetime.date(2024, 5, 31)
        assert creditcard_aura.holder == "Fulano Silva"
        assert creditcard_aura.number == "5006114021788551"
        assert creditcard_aura.brand == "aura"
        assert creditcard_aura.cvv is None

    @freeze_time("2023-11-26")
    def test_exp_date_in_past(self):
        with pytest.raises(ValueError) as e:
            CreditCard(
                exp_date=datetime.date(1998, 11, 20),
                holder="Ciclano F Souza",
                number="5006114021788551",
            )

        assert str(e.value) == "Expiration date must be a future date!"

    @freeze_time("2023-12-11")
    def test_not_month_last_day(self):
        with pytest.raises(ValueError) as e:
            CreditCard(
                exp_date=datetime.date(2025, 10, 1),
                holder="Fulano de Tal",
                number="5400437724026876",
            )

        assert (
            str(e.value)
            == "The day in expiration date must be the last one in the month!"
        )

    @freeze_time("2023-11-26")
    def test_invalid_number(self):
        with pytest.raises(ValueError) as e:
            CreditCard(
                exp_date=datetime.date(2024, 5, 31),
                holder="Jojisnei Camargo",
                number="0123456789112233",
            )

        assert str(e.value) == "The card number isn't valid!"

    @freeze_time("2023-12-11")
    @pytest.mark.parametrize("exp_date", ["05/2025", datetime.date(2025, 5, 31)])
    def test_create_factory(self, exp_date: str | datetime.date):
        card = CreditCard.create(
            exp_date=exp_date,
            holder="Fulano de Tal",
            number="5406183511065370",
            cvv=851,
        )

        assert card.exp_date == datetime.date(2025, 5, 31)
        assert card.holder == "Fulano de Tal"
        assert card.number == "5406183511065370"
        assert card.cvv == 851

    @pytest.mark.parametrize(
        "exp_date",
        [
            "11/05/2025",
            "5/2025",
            "2025/05",
            "2025/5",
            "2025/05/11",
            "2025/11/05",
        ],
    )
    def test_create_factory_with_wrong_str_date_format(self, exp_date: str):
        with pytest.raises(ValueError) as e:
            CreditCard.create(
                exp_date=exp_date,
                holder="Fulano de Tal",
                number="5406183511065370",
                cvv=851,
            )

        assert (
            str(e.value) == "The date parameter must be in the following format %m/%Y"
        )
