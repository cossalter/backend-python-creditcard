import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

URL_CONNECTION = os.getenv("DATABASE_URL_CONNECTION")
engine = create_engine(
    URL_CONNECTION,
    connect_args={"check_same_thread": False}
    if URL_CONNECTION.startswith("sqlite")
    else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
