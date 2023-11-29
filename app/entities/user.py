from dataclasses import dataclass

from base.entity import BaseEntity


@dataclass
class User(BaseEntity):
    username: str
    password: str
    is_active: bool

    def confirm_password(self, password: str) -> bool:
        return self.password == password

    def validation(self) -> None:
        pass
