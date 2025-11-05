import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.log_decorator import log
from db_connection import DBConnection
import logging
from business_object.user import User


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
                        user.user_id = res[0]
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

    @log
    def login(self, username, password) -> User:
        """To connect with username and password

        Parameters
        ----------
        pseudo : str
            pseudo du joueur que l'on souhaite trouver
        mdp : str
            mot de passe du joueur

        Returns
        -------
        joueur : Joueur
            renvoie le joueur que l'on cherche
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM joueur                      "
                        " WHERE pseudo = %(pseudo)s         "
                        "   AND mdp = %(mdp)s;              ",
                        {"pseudo": pseudo, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        joueur = None

        if res:
            joueur = Joueur(
                pseudo=res["pseudo"],
                mdp=res["mdp"],
                age=res["age"],
                mail=res["mail"],
                fan_pokemon=res["fan_pokemon"],
                id_joueur=res["id_joueur"],
            )

        return joueur