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