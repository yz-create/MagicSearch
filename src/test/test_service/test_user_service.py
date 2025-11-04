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

def test_create_user_success():
    """Successful user creation"""

    # GIVEN
    username, password = "jp", "1234"
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.create.return_value = "CREATED"
    service = UserService(user_dao=mock_dao)

    # WHEN
    user = service.create_user(username, password)

    # THEN
    mock_dao.create.assert_called_once()
    assert isinstance(user, User)
    assert user.username == username


def test_create_user_exists():
    """User creation fails because username already exists"""

    # GIVEN
    username, password = "lea", "0000"
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.create.return_value = "EXISTS"
    service = UserService(user_dao=mock_dao)

    # WHEN
    user = service.create_user(username, password)

    # THEN
    mock_dao.create.assert_called_once()
    assert user is None


def test_create_user_error():
    """User creation fails because of a generic error"""

    # GIVEN
    username, password = "gg", "abcd"
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.create.return_value = "ERROR"
    service = UserService(user_dao=mock_dao)

    # WHEN
    user = service.create_user(username, password)

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


def test_find_by_username_exists():
    """Find user by username (exists)"""

    # GIVEN
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.get_by_username.return_value = user_list[1]  # user "lea"
    service = UserService(user_dao=mock_dao)

    # WHEN
    user = service.find_by_username("lea")

    # THEN
    mock_dao.get_by_username.assert_called_once_with("lea")
    assert user.username == "lea"


def test_find_by_username_not_exists():
    """Find user by username (does not exist)"""

    # GIVEN
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.get_by_username.return_value = None
    service = UserService(user_dao=mock_dao)

    # WHEN
    user = service.find_by_username("kitten")

    # THEN
    mock_dao.get_by_username.assert_called_once_with("kitten")
    assert user is None


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
