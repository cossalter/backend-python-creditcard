import datetime

from dataclasses import dataclass

from base.entity import BaseEntity


@dataclass
class User(BaseEntity):
    username: str
    hashed_password: str
    doc: str
    birthday: datetime.date
    is_active: bool

    @property
    def age(self) -> int:
        return (datetime.date.today() - self.birthday).days // 365

    def validation(self) -> None:
        pass
