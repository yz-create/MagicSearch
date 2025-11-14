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
        query = 'SELECT "username", "isAdmin" FROM defaultdb."User";'
        rows = []
        try:
            with self.db.connection as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
        except Exception as e:
            logging.error(f"Error reading all users: {e}")
        return [{"username": r["username"], "isAdmin": r["isAdmin"]} for r in rows]

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


#####A FINIR########
    @log
    def delete(self, username: str):
        """
        Delete an user according to their username.
        
        Parameters
        ----------
        username (str): username of the user to delete
        
        Returns
        -------
        the informations about the user deleted
        """
        try:
            with self.db.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT "idUser", "username", "password", "isAdmin" FROM defaultdb."User" WHERE;')
                    rows = cursor.fetchall()
        pass

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

    def add_favourite_card(self, user_id: int, idCard: int) -> str:
        try:
            conn = self.db.connection

            with conn.cursor() as cursor:
                # check if the idCard already is in the list
                cursor.execute(
                    'SELECT 1 FROM defaultdb."Favourite" WHERE "idUser" = %(user_id)s AND  "idCard"= %(idCard)s;',
                    {"user_id": user_id, "idCard": idCard}
                )
                if cursor.fetchone() is not None:
                    return "EXISTS"

                # insertion
                cursor.execute(
                    """
                    INSERT INTO defaultdb."Favourite" ("idUser", "idCard")
                    VALUES (%(user_id)s, %(idCard)s)
                    RETURN idCard;
                    """,
                    {"user_id": user_id, "idCard": idCard}
                )
                res = cursor.fetchone()
                print("Fetchone result after insertion :", res)  # <- debug
                # check whether it has been added
                user = User()
                if UserDao.add_favourite_card(user_id, idCard) == None:
                    user.user_id = res["idUser"]
                    conn.commit()
                    print("User créé avec ID :", user.user_id)  # <- debug
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
