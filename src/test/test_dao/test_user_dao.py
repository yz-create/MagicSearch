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