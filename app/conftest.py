import pytest

from main import app

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base

client = TestClient(app)


# Create database session for tests
@pytest.fixture
def _create_db_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    return session


@pytest.fixture
def db_session(_create_db_session):
    db = _create_db_session()

    try:
        yield db
    finally:
        db.close()
