from tabulate import tabulate

from utils.log_decorator import log
from utils.security import hash_password

from business_object.user import User
from dao.user_dao import UserDao


class UserService:
    """Class containing user service methods"""

    @log
    def create(self, username, password) -> User:
        """Create a user from its attributes"""

        new_user = User(
            username=username,
            password=hash_password(password, username)
        )

        return new_user if UserDao().create(new_user) else None

    @log
    def list_all(self, include_password=False) -> list[User]:
        """List all users
        If include_password=True, passwords will be included.
        By default, all user passwords are set to None.
        """
        users = UserDao().list_all()
        if not include_password:
            for u in users:
                u.password = None
        return users

    @log
    def find_by_id(self, user_id) -> User:
        """Find a user by its ID"""
        return UserDao().find_by_id(user_id)

    @log
    def update(self, user) -> User:
        """Update a user"""

        user.password = hash_password(user.password, user.username)
        return user if UserDao().update(user) else None

    @log
    def delete(self, user) -> bool:
        """Delete a user account"""
        return UserDao().delete(user)

    @log
    def display_all(self) -> str:
        """Display all users
        Output: A formatted string table
        """
        headers = ["username", "age", "email", "is admin"]

        users = UserDao().list_all()

        for u in users:
            if u.username == "admin":
                users.remove(u)

        users_as_list = [u.as_list() for u in users]

        str_users = "-" * 100
        str_users += "\nList of users\n"
        str_users += "-" * 100
        str_users += "\n"
        str_users += tabulate(
            tabular_data=users_as_list,
            headers=headers,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_users += "\n"

        return str_users

    @log
    def login(self, username, password) -> User:
        """Login using username and password"""
        return UserDao().login(username, hash_password(password, username))

    @log
    def username_already_used(self, username) -> bool:
        """Check if the username is already used.
        Returns True if the username already exists in the database.
        """
        users = UserDao().list_all()
        return username in [u.username for u in users]
