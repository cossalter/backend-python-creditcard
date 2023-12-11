import datetime

from entities.user import User
from entities.credit_card import CreditCard

from freezegun import freeze_time


class TestUserEntity:
    def test_create(self):
        user = User(username="fulaninho", is_active=True)

        assert user.username == "fulaninho"
        assert user.is_active is True

    @freeze_time("2023-12-11")
    def test_add_card(self):
        user = User(username="fulaninho", is_active=True)

        cards = [
            CreditCard(
                exp_date=datetime.date(2025, 10, 31),
                holder="Fulano de Tal",
                number="5400437724026876",
                cvv=871,
            ),
            CreditCard(
                exp_date=datetime.date(2024, 6, 30),
                holder="Fulano de Tal",
                number="5276334697446499",
                cvv=537,
            ),
        ]

        for card in cards:
            user.add_card(card)

        assert user.cards == cards
