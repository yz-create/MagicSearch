from tabulate import tabulate

from utils.log_decorator import log
from utils.security import hash_password

from business_object.user import User
from dao.user_dao import UserDao
from db_connection import DBConnection


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
        """Create a new user and handle duplicate username."""
        hashed_password = hash_password(password, username)
        new_user = User(username=username, password=hashed_password)       
        if self.dao.create(new_user):
            print(f"User '{username}' created successfully!")
            return new_user
        else:    
            print(f"Username '{username}' already exists!")
            return None

    @log
    def list_all(self, include_password: bool = False) -> list[User]:
        """List all users. Hide passwords by default."""
        users = self.user_dao.list_all() or []

        if not include_password:
            for user in users:
                user.password = None

        return users

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
        """Login using username and password."""
        user = self.user_dao.get_by_username(username)
        if not user:
            return None

        hashed_input_pw = hash_password(password, username)
        if user.password == hashed_input_pw:
            return user
        return None

    @log
    def username_already_used(self, username: str) -> bool:
        """Check if a username is already used."""
        existing_user = self.user_dao.get_by_username(username)
        return existing_user is not None
