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

    @patch("dao.user_dao.DBConnection")
    def test_get_by_id_user_found(self, mock_db_connection):
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
        user = dao.get_by_id("idUser")

        #THEN
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "secret")
        self.assertFalse(user.is_admin)
        mock_cursor.execute.assert_called_once()

    
    @patch("dao.user_dao.DBConnection")
    def test_get_by_id_user_not_found(self, mock_db_connection):
        # GIVEN
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
    
        mock_cursor.rowcount = 1
    
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_db_connection.return_value.connection.__enter__.return_value = mock_connection
    
        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)

        #WHEN
        user = dao.get_by_id(4022)

        #THEN
        self.assertIsNone(user)
        mock_cursor.execute.assert_called_once()

    @patch("dao.user_dao.DBConnection")
    def test_get_by_id_db_error(self, mock_db_connection):
        # GIVEN
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Database error")
    
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    
        mock_db_connection.return_value.connection.__enter__.return_value = mock_connection
    
        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)

        # WHEN
        user = dao.get_by_id(1)

        # THEN
        self.assertIsNone(user)
        mock_cursor.execute.assert_called_once()

    # -------------------------------------------------------------------
    # TESTS update
    # -------------------------------------------------------------------

    @patch("dao.user_dao.DBConnection")
    def test_update_user_not_found(self, mock_db_connection):
        """L'utilisateur n'existe pas -> return None"""

        # Mock connexion + curseur
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_db_connection.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Le SELECT renvoie None
        mock_cursor.fetchone.return_value = None

        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)
        
        res = dao.update(1, "new", "pwd")

        # 1 seul appel : SELECT
        mock_cursor.execute.assert_called_once()
        self.assertIsNone(res)

    @patch("dao.user_dao.DBConnection")
    def test_update_user_success(self, mock_db_connection):
        """Mise à jour complète OK"""

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_db_connection.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # 1er fetch : utilisateur existant
        mock_cursor.fetchone.side_effect = [
            {
                "idUser": 1,
                "username": "old",
                "password": "123",
                "isAdmin": False
            },
            {
                "idUser": 1,
                "username": "new_username",
                "password": "new_pwd",
                "isAdmin": False
            }
        ]

        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)
        
        res = dao.update(1, "new_username", "new_pwd")

        # Vérification de la valeur retournée
        self.assertIsInstance(res, User)
        self.assertEqual(res.user_id, 1)
        self.assertEqual(res.username, "new_username")
        self.assertEqual(res.password, "new_pwd")
        self.assertFalse(res.is_admin)

        # Vérification que la requête UPDATE a bien été appelée
        update_call = mock_cursor.execute.call_args_list[1]  # le 2e appel
        query, params = update_call[0][0], update_call[0][1]

        self.assertIn("UPDATE", query)
        self.assertEqual(params, ("new_username", "new_pwd", 1))

    @patch("dao.user_dao.DBConnection")
    def test_update_user_update_failed(self, mock_db_connection):
        """SELECT OK mais UPDATE retourne None -> échec"""

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_db_connection.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # SELECT renvoie un utilisateur
        mock_cursor.fetchone.side_effect = [
            {"idUser": 1, "username": "old", "password": "pwd", "isAdmin": False},
            None   # UPDATE RETURNING -> None
        ]

        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)
        
        res = dao.update(1, "x", "y")

        self.assertIsNone(res)

    @patch("dao.user_dao.DBConnection")
    def test_update_user_exception(self, mock_db_connection):
        """Une exception SQL doit renvoyer None"""

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_db_connection.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Simuler une exception lors du SELECT
        mock_cursor.execute.side_effect = Exception("SQL ERROR")

        fake_db = mock_db_connection.return_value
        dao = UserDao(fake_db)
        
        res = dao.update(1, "x", "y")

        self.assertIsNone(res)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])