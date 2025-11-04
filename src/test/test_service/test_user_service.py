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
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.create.return_value = True
    service = UserService(user_dao=mock_dao)

    # WHEN
    user = service.create(username, password)

    # THEN
    mock_dao.create.assert_called_once()
    assert isinstance(user, User)
    assert user.username == username


def test_create_failure():
    """User creation failed (because UserDao.create returns False)"""

    # GIVEN
    username, password = "jp", "1234"
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.create.return_value = False
    service = UserService(user_dao=mock_dao)

    # WHEN
    user = service.create(username, password)

    # THEN
    mock_dao.create.assert_called_once()
    assert user is None


def test_list_all_include_password_true():
    """List users including passwords"""

    # GIVEN
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.list_all.return_value = user_list
    service = UserService(user_dao=mock_dao)

    # WHEN
    res = service.list_all(include_password=True)

    # THEN
    mock_dao.list_all.assert_called_once()
    assert len(res) == 3
    for user in res:
        assert user.password is not None


def test_list_all_include_password_false():
    """List users excluding passwords"""

    # GIVEN
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.list_all.return_value = [User(u.username, u.password) for u in user_list]
    service = UserService(user_dao=mock_dao)

    # WHEN
    res = service.list_all(include_password=False)

    # THEN
    mock_dao.list_all.assert_called_once()
    assert len(res) == 3
    for user in res:
        assert user.password is None


def test_username_already_used_yes():
    """Username already exists"""

    # GIVEN
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.get_by_username.return_value = user_list[1]  # user "lea"
    service = UserService(user_dao=mock_dao)

    # WHEN
    res = service.username_already_used("lea")

    # THEN
    mock_dao.get_by_username.assert_called_once_with("lea")
    assert res is True


def test_username_already_used_no():
    """Username does not exist"""

    # GIVEN
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.get_by_username.return_value = None
    service = UserService(user_dao=mock_dao)

    # WHEN
    res = service.username_already_used("kitten")

    # THEN
    mock_dao.get_by_username.assert_called_once_with("kitten")
    assert res is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
