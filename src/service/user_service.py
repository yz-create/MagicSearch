from tabulate import tabulate

from utils.log_decorator import log
from utils.security import hash_password

from business_object.user import User
from card_service import CardService
from dao.user_dao import UserDao
from db_connection import DBConnection
import logging
from psycopg2.extras import DictCursor
from fastapi import HTTPException, Depends


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
        if not current_user.is_admin:
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

    def add_favourite_card(self, user_id : int, idCard:int): 
        """"Check whether the idCard exists and adds it to the list of 
        favourite cards of the user corresponding to idUser
        
        Parameters :
        ------------
        user_id : int
            id of the user calling the method
            
        idCard : int
            id of the card, that the user wants to add to their favourites
        """
        try: 
            if CardService.id_search(idCard) == None: 
                raise ValueError("This idCard doesn't match any card... try again !")
            else: 
                add = self.user_dao.add_favourite_card(user_id, idCard)
                if result == "ADDED":
                    print(f"The card '{idCard}' had been added to your favourites!")
                    return idCard
                elif result == "EXISTS":
                    print(f"The card '{idCard}' is already!")
                    return None
                else:
                    print(f"Error creating user '{username}'. Please try again later.")
                    return None

        except :
