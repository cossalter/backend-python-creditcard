import datetime

from base.utils import decrypt

from entities.credit_card import CreditCard

from sqlalchemy.orm import Session

from database.models.credit_card import CreditCardModel


class TestCreditCard:
    def test_create_model(self, db_session: Session):
        card = CreditCard(
            exp_date=datetime.date(2024, 5, 31),
            holder="Fulano Tal",
            number="5478473386028568",
            cvv=128,
        )

        card_model = CreditCardModel.create(db_session, card)
        assert card_model.id is not None
        assert card_model.exp_date == datetime.date(2024, 5, 31)
        assert card_model.holder == "Fulano Tal"
        assert card_model.cvv == 128

        # Decrypt and check the card number
        assert decrypt(card_model.number) == "5478473386028568"

    def test_create_batch_models(self, db_session):
        cards = [
            CreditCard(
                exp_date=datetime.date(2024, 5, 31),
                holder="Fulano Tal",
                number="5478473386028568",
                cvv=128,
            ),
            CreditCard(
                exp_date=datetime.date(2024, 3, 31),
                holder="Beltrano C Camargo",
                number="5059578975747662",
                cvv=None,
            ),
        ]

        card_batch = CreditCardModel.create_batch(db_session, cards)

        assert CreditCardModel.filter(db_session).all() == card_batch

    def test_get_specific_credit_card(self, db_session):
        cards = [
            CreditCard(
                exp_date=datetime.date(2024, 5, 31),
                holder="Fulano Tal",
                number="5478473386028568",
                cvv=128,
            ),
            CreditCard(
                exp_date=datetime.date(2024, 3, 31),
                holder="Beltrano C Camargo",
                number="5059578975747662",
                cvv=None,
            ),
        ]

        card_batch = CreditCardModel.create_batch(db_session, cards)

        card_model1 = CreditCardModel.get(db_session, id=card_batch[0].id)
        assert card_model1.id is not None
        assert card_model1.exp_date == datetime.date(2024, 5, 31)
        assert card_model1.holder == "Fulano Tal"
        assert decrypt(card_model1.number) == "5478473386028568"
        assert card_model1.cvv == 128

        card_model2 = CreditCardModel.get(db_session, id=card_batch[1].id)
        assert card_model2.id is not None
        assert card_model2.exp_date == datetime.date(2024, 3, 31)
        assert card_model2.holder == "Beltrano C Camargo"
        assert decrypt(card_model2.number) == "5059578975747662"
        assert card_model2.cvv is None
