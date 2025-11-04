import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.log_decorator import log
from db_connection import DBConnection
import logging
from business_object.user import User

class UserDao:
    """Communication between UserService and the DBConnexion"""
    def __init__(self, db):
        self.db = db

    def read_all_user(self):
        """Return all the users"""
        pass

    def get_by_username(self, username: str):
        """Re"""
        pass

    @log
    def create(self, user: User) -> bool:
        """
        Create a new user in the database.

        Parameters
        ----------
        user : User
            The User object to insert into the database.

        Returns
        -------
        created : bool
            True if created successfully, False otherwise
        """
        res = None

        try:
            with self.db.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO "User" (username, password, isAdmin)
                        VALUES (%(username)s, %(password)s, False)
                        RETURNING idUser;
                        """,
                        {
                            "username": user.username,
                            "password": user.password,
                            "isAdmin": False
                        },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.error(f"Error while creating a user: {e}")

        created = False
        if res:
            user.user_id = res["idUser"]
            created = True

        return created

    def delete(self, user_id: int):
        """Supprimer un utilisateur"""
        pass

    def list_all(self):
        """Lister tous les utilisateurs"""
        pass