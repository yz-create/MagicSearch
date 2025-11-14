import logging

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from security.auth import create_access_token, verify_token, verify_admin
from datetime import timedelta
from typing import List, Union

from service.user_service import UserService
from service.card_service import CardService
from utils.log_init import initialize_logs


# SETTING UP THE API
root_path = "/proxy/9876"
app = FastAPI(
    title="MagicSearch",
    root_path=root_path,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

initialize_logs("WebserviceOK")


# path to the documentation
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="docs")

user_service = UserService()
card_service = CardService()


# librairie Pydantic BaseModel
class cardModel(BaseModel): 
    """
    defines a Pydantic model for the uards
    Pydantic model to validate and document the user objects
    received as input and returned as output
    """
    id_card: int
    layout: str
    name: str
    type_line: str
    ascii_name: str | None = None
    color_identity: list | None = None
    color_indicator: list | None = None
    colors: list | None = None
    converted_mana_cost: float | None = None
    defense: int | None = None
    edhrec_rank: int | None = None
    edhrec_saltiness: float | None = None
    face_mana_value: float | None = None
    face_name: str | None = None
    first_printing: str | None = None
    foreign_data: list | None = None
    hand: int | None = None
    has_alternative_deck_limit: bool | None = None
    is_funny: bool | None = None
    is_reserved: bool | None = None
    keywords: list | None = None
    leadership_skills: dict | None = None
    legalities: Union[dict, int] | None = None
    life: int | None = None
    loyalty: str | None = None
    mana_cost: str | None = None
    mana_value: float | None = None
    power: str | None = None
    printings: list | None = None
    purchase_urls: dict | None = None
    rulings: list | None = None
    side: str | None = None
    subtypes: list | None = None
    supertypes: list | None = None
    text: str | None = None
    toughness: str | None = None
    types: list | None = None

class AbstractFilterModel(BaseModel):
    variable_filtered: str
    type_of_filtering: str
    filtering_value: Union[int, str]


class UserCreateRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str


class userModel(BaseModel):
    """
    defines a Pydantic model for the users
    Pydantic model to validate and document the user objects
    received as input and returned as output
    """
    username: str
    password: str


# USER LOG IN
# creating a user
@app.post("/user/", tags=["User : sign up !"])
async def create_user(j: userModel):
    """Create a new user"""
    logging.info("creating a user")

    # Vérifier si le nom d'utilisateur existe déjà
    existing_user = user_service.find_by_username(j.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already used")

    # Créer l'utilisateur
    user = user_service.create_user(j.username, j.password)
    if not user:
        raise HTTPException(status_code=500, detail="Error while creating the user")

    return {"message": f"User '{j.username}' created successfully!"}

# user sign in 

# ajout pour le système de connexion avec token
@app.post("/login", tags=["User : log in !"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentifie un utilisateur et renvoie un JWT.
    Compatible avec Swagger UI (OAuth2 password flow).
    """
    logging.info("Attempting login")

    user = user_service.login(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong username or password")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=1440)
    )

    logging.info(f"User '{user.username}' successfully logged in")
    return {"access_token": access_token, "token_type": "bearer"}

# ROAMING IN THE MAGICSEARCH DATABASE
# get a random card
# Card_Service().view_random_card()
@app.get("/card/", tags=["Roaming in the MagicSearch Database"])
async def view_random():
    """get a random card"""
    logging.info("get a random card")
    return card_service.view_random_card().show_card()


# get a card by its id
# Card_Service().id_search(id)
@app.get("/card/{id}", tags=["Roaming in the MagicSearch Database"])
async def id_search(id: int):
    """Finds a card based on its id """
    logging.info("Finds a card based on its id ")
    return card_service.id_search(id).show_card()


# get a card by its name
# Card_Service().name_search(name)
@app.get("/card/by-name/{name}", tags=["Roaming in the MagicSearch Database"])
async def name_search(name: str):
    """Finds a card based on its name """
    logging.info("Finds a card based on its name")
    cards = card_service.name_search(name)
    cards_as_dict = []
    for card in cards:
        cards_as_dict.append(card.show_card())
    return cards_as_dict


# get the result of a semantic search (Detailed Embed = normal)
# Card_Service().semantic_search(search)
@app.get("/card/semantic/recommended/{search}", tags=["Roaming in the MagicSearch Database"])
async def semantic_search(search):
    """Finds a card based on its a semantic search"""
    logging.info("Finds a card based on its a semantic search (recommended)")
    cards = card_service.semantic_search(search)
    cards_as_dict = []
    for card in cards:
        cards_as_dict.append(card.show_card())
    return cards_as_dict


# get the result of a semantic search (shortEmbed = FO1a)
# Card_Service().semantic_search(search)
@app.get("/card/semantic/short/{search}", tags=["Roaming in the MagicSearch Database"])
async def semantic_search_shortEmbed(search):
    """Finds a card based on its a semantic search"""
    logging.info("Finds a card based on its a semantic search")
    cards = card_service.semantic_search_shortEmbed(search)
    cards_as_dict = []
    for card in cards:
        cards_as_dict.append(card.show_card())
    return cards_as_dict


# get a filtered list of cards
# card_Service().filter_num_service(self, filter: AbstractFilter)
@app.post("/card/AbstractFilterModel", tags=["Roaming in the MagicSearch Database"])
async def filter_search(filters: List[AbstractFilterModel]):
    """Filters the database based on a list of filters"""
    logging.info("Filters the database based on a list of filters")
    cards = card_service.filter_search(filters)
    
    return cards

# add a favourite card
@app.post("/user/add_to_favourite/{idCard}", tags=["Roaming in the MagicSearch Database"])
async def Add_favourite_card(idCard:int, current_user=Depends(verify_token)):
    """Adds a card to the favourite cards of the current user"""
    logging.info("Adds a card to the favourite cards of the current user")
    user_id = current_user.user_id
    return user_service.add_favourite_card(user_id, idCard)

@app.get("/user/see_favourites/", tags=["Roaming in the MagicSearch Database"])
async def List_favourite_cards(current_user=Depends(verify_token)):
    """List all the favourite cards of the current user"""
    logging.info("List all the favourite cards of the current user")
    user_id = current_user.user_id
    return user_service.list_favourite_cards(user_id)

# DATABASE MANAGEMENT :CARDS
# create a card
@app.post("/card/create/cardModel", tags=["Database management : cards"])
async def Create_card(card:cardModel):
    """Creates a card in the Magicsearch database"""
    logging.info("Creates a card in the Magicsearch database")
    return card_service.create_card(card)


# update a card
@app.put("/card/create/cardModel", tags=["Database management : cards"])
async def Update_card(card:cardModel):
    """Updates a card in the Magicsearch database"""
    logging.info("Updates a card in the Magicsearch database")
    return card_service.update_card(card)


# delete a card
@app.delete("/card/delete/cardModel}", tags=["Database management : cards"])
async def Delete_card(card: cardModel):
    """Deletes a card in the Magicsearch database"""
    logging.info("Deletes a card in the Magicsearch database")
    return card_service.delete_card(card)


# DATABASE MANAGEMENT : USER
# routes utilisateurs : get user et get user id
# list the users
# protéger fonctions faites que pour admin
# list all users

@app.get("/user/", tags=["Database management : user"])
async def list_all_users(current_user=Depends(verify_admin)):
    """List all users, only for admins."""
    logging.info(f"List all users requested by {getattr(current_user, 'username', current_user)}")
    return user_service.list_all(current_user)

# delete a user

@app.delete("/user/{id_user}", tags=["Database management : user"])
def delete_user(username: str, current_user=Depends(verify_admin)):
    """Deleting a user, only for admins."""
    logging.info(f"Suppression de l'utilisateur {username} par {current_user}")
    user = user_service.find_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete(user)
    return f"User {user.username} deleted"


# fin modif pour connexion et token


# @app.get("/user/", tags=["Database management : user"])
# async def list_all_users():
#     """Lister tous les users"""
#     logging.info("List all users")
#     list_users = user_service.list_all()
#
#     liste_model = []
#     for user in list_users:
#         liste_model.append(user)
#
#     return liste_model


# get a user by their id
@app.get("/user/{user_id}", tags=["Database management : user"])
async def user_by_id(user_id: int):
    """Finds a user based on their id """
    logging.info("Finds a user based on their id")
    return user_service.find_by_id(user_id)


# updating of a user
@app.put("/user/{id_user}", tags=["Database management : user"])
def update_user(id_user: int, j: userModel):
    """updating of a user"""
    logging.info(f"updating of user {id_user}")
    user = user_service.trouver_par_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    user.username = j.username
    user.password = j.password
    user = user_service.modifier(user)
    if not user:
        raise HTTPException(status_code=404, detail="Error while updating user")

    return f"user {j.username} updated"


# deleting a user
# @app.delete("/user/{id_user}", tags=["Database management : user"])
# def Delete_user(id_user: int):
#     """Deleting a user"""
#     logging.info(f"Deleting user {id_user}")
#     user = user_service.trouver_par_id(id_user)
#     if not user:
#         raise HTTPException(status_code=404, detail="user not found")
#
#     user_service.supprimer(user)
#     return f"user {user.username} deleted"


# API TEST
# @app.get("/hello/{name}")
#async def hello_name(name: str):
#    """Afficher Hello"""
#    logging.info(f"Afficher Hello {name}")
#    return f"message : Hello {name}"

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
