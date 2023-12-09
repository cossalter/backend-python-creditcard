from dataclasses import dataclass, field

from base.entity import BaseEntity

from entities.credit_card import CreditCard


@dataclass
class User(BaseEntity):
    username: str
    is_active: bool
    cards: list[CreditCard] = field(init=False, default_factory=list)

    def validation(self) -> None:
        pass

    def add_card(self, card: CreditCard) -> None:
        self.cards.append(card)
