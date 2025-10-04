from db_connection import DBConnection

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

    def create(self, username: str, email: str, password: str):
        """Créer un nouvel utilisateur"""
        pass

    def delete(self, user_id: int):
        """Supprimer un utilisateur"""
        pass

    def list_all(self):
        """Lister tous les utilisateurs"""
        pass