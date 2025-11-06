import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from unittest.mock import MagicMock, patch
from business_object.user import User
from dao.user_dao import UserDao
from db_connection import DBConnection


class TestUserDao(unittest.TestCase):

    def test_create_user_success(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [None, {"idUser": 42}]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_db = MagicMock()
        mock_db.connection.__enter__.return_value = mock_connection

        user = User(username="test_username", password="test_password")
        dao = UserDao(mock_db)

        result = dao.create(user)

        self.assertEqual(result, "CREATED")
        self.assertEqual(user.user_id, 42)
        mock_cursor.execute.assert_called()
        mock_cursor.fetchone.assert_called()

    def test_create_user_failure(self):
        mock_db = MagicMock()
        mock_db.connection.__enter__.side_effect = Exception("DB error")

        user = User(username="test_username", password="test_password")
        dao = UserDao(mock_db)

        result = dao.create(user)

        self.assertEqual(result, "ERROR")
        self.assertIsNone(user.user_id)

if __name__ == "__main__":
    unittest.main()

def test_get_username_and_password_res():

    #GIVEN
    username,password='abc','def'
    user= User(username=username, password=password)
    DBConnection().connection = MagicMock(return_value=res)
    
    #WHEN

@patch("user_dao.DBConnection")
def test_get_username_and_password_none(mock_db_connection):
    #GIVEN
        fake_row = {
        "idUser": 1,
        "username": "testuser",
        "password": "secret",
        "isAdmin": False
    }
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = fake_row

    mock_connection = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_db_connection.return_value.connection.__enter__.return_value = mock_connection

    dao = UserDao()
    #WHEN
    result = UserDao(db : DBConnection).get_username_and_password(username, password)

    # THEN
    assert isinstance(user, User)
    assert user.user_id == 1
    assert user.username == "testuser"
    assert user.password == "secret"
    assert user.is_admin is False
    mock_cursor.execute.assert_called_once()
