from entities.user import User


class TestUserEntity:
    def test_create_user_entity(self):
        user = User(
            username="fulaninho",
            password="teste123",
            is_active=True,
        )

        assert user.username == "fulaninho"
        assert user.password == "teste123"
        assert user.is_active is True

    def test_user_confirm_password(self):
        user = User(
            username="foobar",
            password="teste123",
            is_active=True,
        )

        assert user.confirm_password("teste123")

        # Not the same password
        assert not user.confirm_password("123456")
