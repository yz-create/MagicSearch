import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.log_decorator import log
from db_connection import DBConnection
import logging

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
    def create(self, username: str, email: str, password: str) -> bool:
        """
        Crée un nouvel utilisateur (joueur) dans la base de données.

        Parameters
        ----------
        username : str
        Le nom d'utilisateur du joueur
        email : str
        L'adresse e-mail du joueur
        password : str
        Le mot de passe du joueur (idéalement déjà haché)

        Returns
        -------
        created : bool
        True si la création est un succès, False sinon
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO joueur (pseudo, mail, mdp)
                        VALUES (%(pseudo)s, %(mail)s, %(mdp)s)
                        RETURNING user_id;
                        """,
                        {
                            "username": username,
                            "mail": email,
                            "password": password,
                        },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.error(f"Erreur lors de la création du joueur : {e}")

        created = False
        if res:
            self.id_joueur = res["id_joueur"]
            created = True

        return created

    def delete(self, user_id: int):
        """Supprimer un utilisateur"""
        pass

    def list_all(self):
        """Lister tous les utilisateurs"""
        pass