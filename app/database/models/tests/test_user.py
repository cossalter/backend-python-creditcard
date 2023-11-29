from sqlalchemy.orm import Session

from entities.user import User

from database.models.user import create_user, get_user
from base.utils import verify_password


class TestUserModel:
    def test_create_user(self, db_session: Session):
        user = User(
            username="fulaninho",
            password="foobar",
            is_active=True,
        )

        user_from_db = create_user(db_session, user)

        assert isinstance(user_from_db, User)
        assert user_from_db.username == "fulaninho"
        assert user_from_db.is_active is True

        assert user_from_db.password != "foobar"
        assert verify_password("foobar", user_from_db.password)

    def test_get_user(self, db_session: Session):
        user1 = User(
            username="fulaninho",
            password="foobar",
            is_active=True,
        )
        user2 = User(
            username="ciclano",
            password="bean",
            is_active=True,
        )

        create_user(db_session, user1)
        create_user(db_session, user2)

        user_from_db_1 = get_user(db_session, "fulaninho")
        assert user_from_db_1 is not None
        assert user_from_db_1.username == "fulaninho"
        assert verify_password("foobar", user_from_db_1.password)
        assert user_from_db_1.is_active is True

        user_from_db_2 = get_user(db_session, "ciclano")
        assert user_from_db_2 is not None
        assert user_from_db_2.username == "ciclano"
        assert verify_password("bean", user_from_db_2.password)
        assert user_from_db_2.is_active is True
