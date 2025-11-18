import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from unittest.mock import MagicMock, patch
from business_object.user import User
from dao.user_dao import UserDao
from db_connection import DBConnection


class TestUserDao(unittest.TestCase):

    @patch("dao.user_dao.DBConnection")
    def test_get_username_and_password_none(self, mock_db_connection):
        # GIVEN
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

        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)

        # WHEN
        user = dao.get_by_username_and_password("testuser", "secret")

        # THEN
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "secret")
        self.assertFalse(user.is_admin)
        mock_cursor.execute.assert_called_once()

    @patch("dao.user_dao.DBConnection")
    def test_get_by_username(self, mock_db_connection):
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

        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)

        # WHEN
        user = dao.get_by_username("testuser")

        #THEN
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "secret")
        self.assertFalse(user.is_admin)
        mock_cursor.execute.assert_called_once()

    @patch("dao.user_dao.DBConnection")
    def test_delete(self, mock_db_connection):
        # GIVEN
        fake_row = {
            "idUser": 1,
            "username": "testuser",
            "password": "secret",
            "isAdmin": False
        }
    
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = fake_row
    
        mock_cursor.rowcount = 1
    
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_db_connection.return_value.connection.__enter__.return_value = mock_connection
    
        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)

        # WHEN
        result = dao.delete("testuser")
    
        # THEN
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()

    @patch.object(DBConnection, 'connection', autospec=True)
    def test_get_by_id_user_found(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {
            "idUser": 1,
            "username": "testuser",
            "password": "hashedpassword",
            "isAdmin": True
        }

        mock_db = MagicMock()
        mock_db.connection = mock_connection

        dao = UserDao(mock_db)
        user = dao.get_by_id(1)

        self.assertIsInstance(user, User)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_admin)

    @patch.object(DBConnection, 'connection', autospec=True)
    def test_get_by_id_user_not_found(self, mock_db_connection):
        # GIVEN
        fake_row = {
            "idUser": 1,
            "username": "testuser",
            "password": "secret",
            "isAdmin": False
        }
    
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = fake_row
    
        mock_cursor.rowcount = 1
    
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_db_connection.return_value.connection.__enter__.return_value = mock_connection
    
        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)

        #WHEN
        user = dao.get_by_id(999)

        #THEN
        self.assertIsNone(user)

    @patch.object(DBConnection, 'connection', autospec=True)
    def test_get_by_id_db_error(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.side_effect = Exception("Database error")

        mock_db = MagicMock()
        mock_db.connection = mock_connection

        dao = UserDao(mock_db)
        user = dao.get_by_id(1)

        self.assertIsNone(user)



if __name__ == "__main__":
    import pytest
    pytest.main([__file__])