from tabulate import tabulate
from utils.log_decorator import log
from business_object.user import User
from dao.user_dao import UserDao
from fastapi import HTTPException
from db_connection import DBConnection
import logging


class UserService:
    """Class containing user service methods"""

    def __init__(self, user_dao: UserDao = None):
        """Initialize the service with a DAO (can be injected for testing)."""
        if user_dao:
            self.user_dao = user_dao
        else:
            db = DBConnection()
            self.user_dao = UserDao(db)

    @log
    def create_user(self, username: str, password: str) -> User | None:
        new_user = User(username=username, password=password)
        result = self.user_dao.create(new_user)
        if result == "CREATED":
            print(f"User '{username}' created successfully!")
            return new_user
        elif result == "EXISTS":
            print(f"Username '{username}' already exists!")
            return None
        else:
            print(f"Error creating user '{username}'. Please try again later.")
            return None

    @log
    def list_all(self, current_user):
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin rights required")

        return self.user_dao.read_all_user()

    @log
    def find_by_username(self, username: str) -> User | None:
        """Find a user by their username."""
        return self.user_dao.get_by_username(username)

    @log
    def find_by_id(self, user_id: int, current_user) -> User | None:
        """Find a user by their id."""
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin rights required")
        return self.user_dao.get_by_id(user_id)

    @log
    def delete(self, user_id: int) -> bool:
        """Delete a user account by user ID 
        CORRECTION: Signature modifiée pour accepter user_id au lieu de current_user + username.
        La vérification admin devrait être faite dans le contrôleur/route, pas ici.
        """
        return self.user_dao.delete(user_id)

    @log
    def display_all(self) -> str:
        """Display all users as a formatted table."""
        headers = ["Username", "Is Admin"]

        users = self.user_dao.list_all() or []
        users = [u for u in users if u.username != "admin"]

        users_as_list = [u.as_list() for u in users]

        output = "-" * 100 + "\nList of users\n" + "-" * 100 + "\n"
        output += tabulate(
            tabular_data=users_as_list,
            headers=headers,
            tablefmt="psql",
            floatfmt=".2f",
        )
        output += "\n"
        return output

    @log
    def login(self, username: str, password: str) -> User | None:
        user = self.user_dao.get_by_username_and_password(username, password)
        if not user:
            logging.warning(f"Login failed: user {username} not found or wrong password.")
            return None

        logging.info(f"User {username} logged in successfully.")
        return user

    @log
    def update_user(self, user_id: int, username: str, password: str) -> tuple[User] | None:
        """
        Update username and/or password for a user.
        Calls the DAO update function.      
        CORRECTION: Retourne maintenant un tuple (User,) au lieu d'un User directement.
        """
        # Appeler le DAO pour modifier en base
        updated_user = self.user_dao.update(user_id, username, password)

        # Si le DAO retourne None => l'utilisateur n'existe pas ou erreur SQL
        if not updated_user:
            return None

        # CORRECTION: Retourner un tuple contenant l'utilisateur
        return (updated_user,)
