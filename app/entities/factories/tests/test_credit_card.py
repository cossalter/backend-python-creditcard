import datetime
from freezegun import freeze_time

from entities.factories.credit_card import CreditCardFactory
from entities.credit_card import CreditCard


class TestCreditCardFactory:
    @freeze_time("2023-11-26")
    def test_create_credit_card(self):
        # credit card data was generated in:
        # https://www.4devs.com.br/gerador_de_numero_cartao_credito

        factory_card_master = CreditCardFactory.create(
            exp_date="09/2025",
            holder="Fulano da Silva",
            number="5506857222793219",
        )
        creditcard_master = CreditCard(
            exp_date=datetime.date(2025, 9, 30),
            holder="Fulano da Silva",
            number="5506857222793219",
        )

        assert all(
            getattr(factory_card_master, attr) == getattr(creditcard_master, attr)
            for attr in creditcard_master.__dataclass_fields__.keys()
        )
