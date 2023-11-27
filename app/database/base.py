import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


engine = create_engine(
    os.getenv("DATABASE_URL_CONNECTION"),
    connect_args={"check_same_thread": False},
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
