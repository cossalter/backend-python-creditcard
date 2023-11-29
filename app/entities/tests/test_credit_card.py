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

    @freeze_time("2023-11-26")
    def test_invalid_number(self):
        with pytest.raises(ValueError) as e:
            CreditCard(
                exp_date=datetime.date(2024, 5, 31),
                holder="Jojisnei Camargo",
                number="0123456789112233",
            )

        assert str(e.value) == "The card number isn't valid!"
