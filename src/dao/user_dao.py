import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.log_decorator import log
from db_connection import DBConnection
import logging
from business_object.user import User
from psycopg import sql
from psycopg2.extras import DictCursor
from dao.card_dao import CardDao


class UserDao:
    """Communication between UserService and the DBConnexion"""
    def __init__(self, db: DBConnection):
        self.db = db

    def read_all_user(self):
        """Return all users"""
        query = 'SELECT "username", "idUser", "isAdmin" FROM defaultdb."User";'
        rows = []
        try:
            with self.db.connection as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
        except Exception as e:
            logging.error(f"Error reading all users: {e}")
        return [{"username": r["username"], "idUser": r["idUser"], "isAdmin": r["isAdmin"]} for r in rows]

    def get_by_username(self, username: str) -> User | None:
        """Return user corresponding to the username"""
        try:
            with self.db.connection as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(
                        'SELECT "idUser", "username", "password", "isAdmin" '
                        'FROM defaultdb."User" WHERE "username" = %s;',
                        (username,),
                    )
                    res = cursor.fetchone()
            if not res:
                return None

            return User(
                user_id=res["idUser"],
                username=res["username"],
                password=res["password"],
                is_admin=res["isAdmin"],
                )
        except Exception as e:
            logging.error(f"Error querying user by username {username}: {e}")
            return None

    def create(self, user: User) -> str:
        try:
            conn = self.db.connection

            with conn.cursor() as cursor:
                # vérifier si le username existe
                cursor.execute(
                    'SELECT 1 FROM defaultdb."User" WHERE "username" = %(username)s;',
                    {"username": user.username}
                )
                if cursor.fetchone() is not None:
                    return "EXISTS"

                # insertion
                cursor.execute(
                    """
                    INSERT INTO defaultdb."User" ("username", "password", "isAdmin")
                    VALUES (%(username)s, %(password)s, False)
                    RETURNING "idUser";
                    """,
                    {"username": user.username, "password": user.password}
                )
                res = cursor.fetchone()
                print("Résultat fetchone après insertion :", res)
                if res:
                    user.user_id = res["idUser"]
                    conn.commit()
                    print("User créé avec ID :", user.user_id)
                    return "CREATED"
                else:
                    print("Aucun ID retourné par la base !")
                    return "ERROR"

        except Exception as e:
            import logging
            logging.exception("Erreur lors de la création de l'utilisateur")
            return "ERROR"


        except Exception as e:
            import logging
            logging.error(f"Error while creating a user: {e}")
            return "ERROR"


    @log
    def delete(self, username: str) -> bool:
        """
        Delete a user according to their username.
        
        Parameters
        ----------
        username (str): Username of the user to delete
        
        Returns
        -------
        bool: True if deletion was successful, False otherwise
        """
        try:
            with self.db.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'DELETE FROM defaultdb."User" WHERE "username" = %(username)s;',
                        {"username": username}
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error deleting user from database: {e}")
            return False

    @log
    def list_all(self) -> list[User]:
        """
        List all users from the database if token given alllows it ie if the user is an admin.

        Returns
        -------
        list[User]
            A list of User objects, or an empty list if none found or error occurs.
        """
        users = []
        try:
            with self.db.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT "idUser", "username", "password", "isAdmin" FROM defaultdb."User";')
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

    def get_by_username_and_password(self, username: str, password: str) -> User | None:
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

    def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a User by id.

        Returns a User object if id match, else None.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    query = """
                        SELECT "idUser", "username", "password", "isAdmin"
                        FROM defaultdb."User"
                        WHERE "idUser" = %s;
                    """
                    cursor.execute(query, (user_id,))
                    res = cursor.fetchone()

                    if not res:
                        logging.info(f"No user found with id {user_id}")
                        return None

                    user = User(
                        user_id=res["idUser"],
                        username=res["username"],
                        password=res["password"],
                        is_admin=res["isAdmin"]
                    )

                    return user

        except Exception as e:
            logging.error(f"Error querying user by id {user_id}: {e}")
            return None

    def update(self, user_id: int, username: str, password: str) -> User | None:
        """
        Update username and/or password for a given user.

        Returns the updated User object if success, else None.
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:

                    # Vérifier si l'utilisateur existe
                    check_query = """
                        SELECT "idUser", "username", "password", "isAdmin"
                        FROM defaultdb."User"
                        WHERE "idUser" = %s;
                    """
                    cursor.execute(check_query, (user_id,))
                    existing = cursor.fetchone()

                    if not existing:
                        return None  # user non trouvé

                    # Effectuer la mise à jour
                    update_query = """
                        UPDATE defaultdb."User"
                        SET "username" = %s, "password" = %s
                        WHERE "idUser" = %s
                        RETURNING "idUser", "username", "password", "isAdmin";
                    """
                    cursor.execute(update_query, (username, password, user_id))
                    updated = cursor.fetchone()

                    if not updated:
                        return None

        except Exception as e:
            logging.error(f"Error updating user: {e}")
            return None

        # Retourne l'utilisateur mis à jour
        return User(
            user_id=updated["idUser"],
            username=updated["username"],
            password=updated["password"],
            is_admin=updated["isAdmin"]
        )
