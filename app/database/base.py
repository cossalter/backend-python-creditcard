import os

from base.entity import BaseEntity

from fastapi import Depends

from typing import Annotated, TypeAlias, Self

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    DeclarativeBase,
    Mapped,
    Query,
    mapped_column,
    sessionmaker,
)

URL_CONNECTION = os.getenv("DATABASE_URL_CONNECTION")
engine = create_engine(
    URL_CONNECTION,
    connect_args={"check_same_thread": False}
    if URL_CONNECTION.startswith("sqlite")
    else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession: TypeAlias = Annotated[Session, Depends(get_db)]


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        index=True,
        autoincrement="auto",
    )

    @classmethod
    def create(cls, db: Session, *, commit: bool = False, **kwargs) -> Self:
        raise NotImplementedError(f"{cls} not implement the method create!")

    @classmethod
    def create_batch(
        cls,
        db: Session,
        entities: list[BaseEntity],
        **kwargs,
    ) -> list[Self]:
        models = []
        last_entity = entities.pop()

        for entity in entities:
            models.append(cls.create(db, entity, commit=False, **kwargs))

        models.append(cls.create(db, last_entity, commit=True, **kwargs))

        return models

    @classmethod
    def filter(cls, db: Session, **kwargs) -> Query[Self]:
        return db.query(cls).filter_by(**kwargs)

    @classmethod
    def get(cls, db: Session, **kwargs) -> Self | None:
        return cls.filter(db, **kwargs).first()

    def save(self, db: Session, commit: bool = True) -> Self:
        db.add(self)

        if commit:
            db.commit()
            db.refresh(self)

        return self

    def to_entinty(self) -> BaseEntity:
        raise NotImplementedError(
            f"{self.__class__} not implement the method to_entity!"
        )
