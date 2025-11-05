import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.log_decorator import log
from db_connection import DBConnection
import logging
from business_object.user import User
from psycopg import sql
from psycopg2.extras import DictCursor


class UserDao:
    """Communication between UserService and the DBConnexion"""
    def __init__(self, db: DBConnection):
        self.db = db

    def read_all_user(self):
        """Return all users"""
        query = "SELECT username, isAdmin FROM User"
        self.db.cursor.execute(query)
        rows = self.db.cursor.fetchall()
        return [{"username": r[0], "isAdmin": r[1]} for r in rows]

    def get_by_username(self, username: str):
        """Re"""
        pass

    @log
    def create(self, user: User) -> str:
        """
        Create a User in the database.

          Returns:
            "CREATED" if successful
            "EXISTS" if username already exists
            "ERROR" if some other DB error occurs
        """
        try:
            with self.db.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'SELECT 1 FROM "User" WHERE username = %(username)s;',
                        {"username": user.username}
                    )
                    if cursor.fetchone() is not None:
                        return "EXISTS"

                    cursor.execute(
                        """
                        INSERT INTO "User" (username, password, isAdmin)
                        VALUES (%(username)s, %(password)s, False)
                        RETURNING idUser;
                        """,
                        {"username": user.username, "password": user.password}
                    )
                    res = cursor.fetchone()
                    if res:
                        user.user_id = res["idUser"]
                        return "CREATED"
        except Exception as e:
            logging.error(f"Error while creating a user: {e}")
            return "ERROR"

    def delete(self, user_id: int):
        """Supprimer un utilisateur"""
        pass

    @log
    def list_all(self) -> list[User]:
        """
        List all users from the database.

        Returns
        -------
        list[User]
            A list of User objects, or an empty list if none found or error occurs.
        """
        users = []
        try:
            with self.db.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT "idUser", "username", "password", "isAdmin" FROM "User";')
                    rows = cursor.fetchall()

                    for row in rows:
                        users.append(
                            User(
                                user_id=row["idUser"],
                                username=row["username"],
                                password=row["password"],
                                isAdmin=row["isAdmin"],
                            )
                        )

        except Exception as e:
            logging.error(f"Error while listing users: {e}")

        return users

    SCHEMA = "defaultdb"

    @staticmethod
    def get_by_username_and_password(username: str, password: str) -> User | None:
        """
        Retrieve a User by username and password.

        Returns a User object if credentials match, else None.
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    query = """
                        SELECT "idUser", "username", "password", "isAdmin"
                        FROM defaultdb."User"
                        WHERE "username" = %s AND "password" = %s;
                    """
                    cursor.execute(query, (username, password))
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Error querying user: {e}")
            return None

        if not res:
            return None

        user = User(
            user_id=res["idUser"],
            username=res["username"],
            password=res["password"],
            is_admin=res["isAdmin"]
        )

        return user