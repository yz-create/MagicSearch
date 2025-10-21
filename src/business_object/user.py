class User:
    """
    Class representing a User

    Attributes
    ----------
    user_id : int
        Unique identifier of the user
    username : str
        Username of the user
    password : str
        User's password (hashed)
    is_admin : bool
        Indicates if the user is an admin
    """

    def __init__(self, username, password=None, user_id=None, age=None, email=None, is_admin=False):
        """Constructor"""
        self.user_id = user_id
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def __str__(self):
        """Return a string representation of the user"""
        return f"User({self.username})"

    def as_list(self) -> list[str]:
        """Return the user's attributes as a list (used for display in tables)"""
        return [self.username, self.is_admin]
