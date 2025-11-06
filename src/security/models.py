from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    idUser: int
    username: str
    password: str
    isAdmin: bool = False

class UserInDB(User):
    password: str

class UserCreate(BaseModel):
    idUser: int
    username: str
    password: str
    isAdmin: bool = False