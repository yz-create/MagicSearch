from unittest.mock import MagicMock

from service.user_service import UserService
from dao.user_dao import UserDao
from business_object.user import User


# ----- Mock user list -----
user_list = [
    User(username="jp", password="1234"),
    User(username="lea", password="0000"),
    User(username="gg", password="abcd"),
]


# ----- TESTS -----

def test_create_success():
    """Successful user creation"""

    # GIVEN
    username, password = "jp", "1234"
    UserDao().create = MagicMock(return_value=True)

    # WHEN
    user = UserService().create(username, password)

    # THEN
    assert user.username == username


def test_create_failure():
    """User creation failed (because UserDao().create returns False)"""

    # GIVEN
    username, password = "jp", "1234"
    UserDao().create = MagicMock(return_value=False)

    # WHEN
    user = UserService().create(username, password)

    # THEN
    assert user is None


def test_list_all_include_password_true():
    """List users including passwords"""

    # GIVEN
    UserDao().list_all = MagicMock(return_value=user_list)

    # WHEN
    res = UserService().list_all(include_password=True)

    # THEN
    assert len(res) == 3
    for user in res:
        assert user.password is not None


def test_list_all_include_password_false():
    """List users excluding passwords"""

    # GIVEN
    UserDao().list_all = MagicMock(return_value=user_list)

    # WHEN
    res = UserService().list_all()

    # THEN
    assert len(res) == 3
    for user in res:
        assert not user.password


def test_username_already_used_yes():
    """Username already exists in user_list"""

    # GIVEN
    username = "lea"

    # WHEN
    UserDao().list_all = MagicMock(return_value=user_list)
    res = UserService().username_already_used(username)

    # THEN
    assert res


def test_username_already_used_no():
    """Username does not exist in user_list"""

    # GIVEN
    username = "kitten"

    # WHEN
    UserDao().list_all = MagicMock(return_value=user_list)
    res = UserService().username_already_used(username)

    # THEN
    assert not res


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
