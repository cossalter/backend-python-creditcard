from entities.user import User


class TestUserEntity:
    def test_create_user_entity(self):
        user = User(username="fulaninho", is_active=True)

        assert user.username == "fulaninho"
        assert user.is_active is True
