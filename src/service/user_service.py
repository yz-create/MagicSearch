from tabulate import tabulate

from utils.log_decorator import log
from utils.security import hash_password

from business_object.user import User
from dao.user_dao import UserDao
from db_connection import DBConnection
import logging
from psycopg2.extras import DictCursor


class UserService:
    """Class containing user service methods"""

    def __init__(self, user_dao: UserDao = None):
        """Initialize the service with a DAO (can be injected for testing)."""
        if user_dao:
            # Mock or custom DAO for testing
            self.user_dao = user_dao
        else:
            # Default: create a real DAO with a DB connection
            db = DBConnection()
            self.user_dao = UserDao(db)

    @log
    def create_user(self, username: str, password: str) -> User | None:
        #hashed_password = hash_password(password, username)
        #new_user = User(username=username, password=hashed_password)
        new_user = User(username=username, password=password)
    
        result = self.user_dao.create(new_user)
        if result == "CREATED":
            print(f"User '{username}' created successfully!")
            return new_user # j'ai limprssion que ça fait pas le lien avec la couche DAO (lucile)
        elif result == "EXISTS":
            print(f"Username '{username}' already exists!")
            return None
        else:
            print(f"Error creating user '{username}'. Please try again later.")
            return None


    @log
    def list_all(self, current_user):
        if not current_user["isAdmin"]:
            raise HTTPException(status_code=403, detail="Admin rights required")

        return self.user_dao.read_all_user()

    @log
    def find_by_username(self, username: str) -> User | None:
        """Find a user by their username."""
        return self.user_dao.get_by_username(username)

    @log
    def delete(self, user_id: int) -> bool:
        """Delete a user account."""
        return self.user_dao.delete(user_id)

    @log
    def display_all(self) -> str:
        """Display all users as a formatted table."""
        headers = ["Username", "Is Admin"]

        users = self.user_dao.list_all() or []
        # Filter out admin user if needed
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
