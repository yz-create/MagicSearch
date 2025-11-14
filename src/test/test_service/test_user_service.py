from unittest.mock import MagicMock
import pytest

from service.user_service import UserService
from dao.user_dao import UserDao
from business_object.user import User
from fastapi import HTTPException


# -------------------------------------------------------------------
# Fixtures et exemples
# -------------------------------------------------------------------

admin_user = User(username="admin", password="adminpass")
admin_user.is_admin = True

normal_user = User(username="bob", password="pwd")
normal_user.is_admin = False

user_list = [
    User(username="jp", password="1234"),
    User(username="lea", password="0000"),
    User(username="gg", password="abcd"),
]


# -------------------------------------------------------------------
# TESTS create_user
# -------------------------------------------------------------------

def test_create_user_success():
    """User created successfully."""

    mock_dao = MagicMock(spec=UserDao)
    mock_dao.create.return_value = "CREATED"

    service = UserService(user_dao=mock_dao)

    user = service.create_user("jp", "1234")

    mock_dao.create.assert_called_once()
    assert isinstance(user, User)
    assert user.username == "jp"


def test_create_user_exists():
    """Username already exists."""

    mock_dao = MagicMock(spec=UserDao)
    mock_dao.create.return_value = "EXISTS"

    service = UserService(user_dao=mock_dao)

    user = service.create_user("lea", "0000")

    mock_dao.create.assert_called_once()
    assert user is None


def test_create_user_error():
    """DAO returned an unexpected error."""

    mock_dao = MagicMock(spec=UserDao)
    mock_dao.create.return_value = "ERROR"

    service = UserService(user_dao=mock_dao)

    user = service.create_user("gg", "abcd")

    mock_dao.create.assert_called_once()
    assert user is None


# -------------------------------------------------------------------
# TESTS list_all
# -------------------------------------------------------------------

def test_list_all_admin_ok():
    """Admin user can list all users."""

    mock_dao = MagicMock(spec=UserDao)
    mock_dao.read_all_user.return_value = user_list

    service = UserService(user_dao=mock_dao)

    res = service.list_all(current_user=admin_user)

    mock_dao.read_all_user.assert_called_once()
    assert res == user_list


def test_list_all_non_admin_forbidden():
    """Non-admin user cannot list users."""

    mock_dao = MagicMock(spec=UserDao)

    service = UserService(user_dao=mock_dao)

    with pytest.raises(HTTPException) as exc:
        service.list_all(current_user=normal_user)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Admin rights required"


# -------------------------------------------------------------------
# TESTS find_by_username
# -------------------------------------------------------------------

def test_find_by_username_exists():
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.get_by_username.return_value = user_list[1]

    service = UserService(user_dao=mock_dao)

    user = service.find_by_username("lea")

    mock_dao.get_by_username.assert_called_once_with("lea")
    assert user.username == "lea"


def test_find_by_username_not_found():
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.get_by_username.return_value = None

    service = UserService(user_dao=mock_dao)

    user = service.find_by_username("unknown")

    mock_dao.get_by_username.assert_called_once_with("unknown")
    assert user is None


# -------------------------------------------------------------------
# TEST delete
# -------------------------------------------------------------------

def test_delete_success():
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.delete.return_value = True

    service = UserService(user_dao=mock_dao)

    res = service.delete(42)

    mock_dao.delete.assert_called_once_with(42)
    assert res is True


def test_delete_fail():
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.delete.return_value = False

    service = UserService(user_dao=mock_dao)

    res = service.delete(42)

    mock_dao.delete.assert_called_once_with(42)
    assert res is False


# -------------------------------------------------------------------
# TEST display_all
# -------------------------------------------------------------------

def test_display_all_formats_table():
    """Table formatting should be returned as a string."""

    mock_dao = MagicMock(spec=UserDao)
    mock_dao.list_all.return_value = user_list

    service = UserService(user_dao=mock_dao)

    output = service.display_all()

    assert isinstance(output, str)
    assert "List of users" in output
    assert "jp" in output
    assert "lea" in output
    assert "gg" in output


# -------------------------------------------------------------------
# TEST login
# -------------------------------------------------------------------

def test_login_success():
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.get_by_username_and_password.return_value = admin_user

    service = UserService(user_dao=mock_dao)

    res = service.login("admin", "adminpass")

    mock_dao.get_by_username_and_password.assert_called_once_with("admin", "adminpass")
    assert res == admin_user


def test_login_fail():
    mock_dao = MagicMock(spec=UserDao)
    mock_dao.get_by_username_and_password.return_value = None

    service = UserService(user_dao=mock_dao)

    res = service.login("admin", "wrongpwd")

    mock_dao.get_by_username_and_password.assert_called_once_with("admin", "wrongpwd")
    assert res is None
