from sqlalchemy.orm import Session

from entities.user import User

from database.models.user import UserModel, get_user
from base.utils import verify_password


class TestUserModel:
    def test_create_user(self, db_session: Session):
        user = User(username="fulaninho", is_active=True)

        user_model = UserModel.create(db_session, user, "foobar")

        assert isinstance(user_model, UserModel)
        assert user_model.username == "fulaninho"
        assert user_model.is_active is True

        assert user_model.password != "foobar"
        assert verify_password("foobar", user_model.password)

    def test_get_user(self, db_session: Session):
        user1 = User(username="fulaninho", is_active=True)
        user2 = User(username="ciclano", is_active=True)

        UserModel.create(db_session, user1, "foobar")
        UserModel.create(db_session, user2, "bean")

        user_model1 = get_user(db_session, user1)
        assert user_model1 is not None
        assert user_model1.username == "fulaninho"
        assert verify_password("foobar", user_model1.password)
        assert user_model1.is_active is True

        user_model2 = get_user(db_session, user2)
        assert user_model2 is not None
        assert user_model2.username == "ciclano"
        assert verify_password("bean", user_model2.password)
        assert user_model2.is_active is True
