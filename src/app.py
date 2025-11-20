import logging

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from security.auth import create_access_token, verify_token, verify_admin
from datetime import timedelta
from typing import List, Union

from service.user_service import UserService
from service.card_service import CardService
from utils.log_init import initialize_logs

tags = [
    {
        "name": "User : sign up !",
        "description": "User registration method",
    },
    {
        "name": "User : log in !",
        "description": "User authentication method : generate 24h token",
    },
    {
        "name": "Roaming in the MagicSearch Database",
        "description": "Browse and search cards",
    },
    {
        "name": "Your very own favourite cards list",
        "description": "Management of the User's favourite cards list ",
    },
    {
        "name": "Database management : cards",
        "description": "Admin operations for card management",
    },
    {
        "name": "Database management : user",
        "description": "Admin operations for user management",
    },
]
# SETTING UP THE API
root_path = "/proxy/9876"
app = FastAPI(
    title="MagicSearch",
    root_path=root_path,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=tags
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
    foreign_data: list[dict] | None = None
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
    rulings: list[dict] | None = None
    side: str | None = None
    subtypes: list | None = None
    supertypes: list | None = None
    text: str | None = None
    toughness: str | None = None
    types: list | None = None


class FilterModel(BaseModel):
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


# get a filtered list of cards : here instead of showing ALL the cards that match the filters we
# page the result !
# card_Service().filter_num_service(self, filter: Filter)
@app.post("/card/filter/{filterModel, page}", tags=["Roaming in the MagicSearch Database"])
async def filter_search(
    filters: List[FilterModel],
    page: int = Query(1, ge=1, description="Page number")
     ):
    """
    Filters with pagination - allows you to get the result of a filter quickly even if it returns
    thousands of results
    """
    logging.info(f"Filtering with {len(filters)} filters, page {page}")

    result = card_service.filter_search(filters, page)
    return result


# FAVOURITE CARDS
# add a favourite card
@app.post("/user/add_to_favourite/{idCard}", tags=["Your very own favourite cards list"])
async def Add_favourite_card(idCard: int, current_user=Depends(verify_token)):
    """Adds a card to the favourite cards of the current user"""
    logging.info("Adds a card to the favourite cards of the current user")
    user_id = current_user.user_id
    return card_service.add_favourite_card(user_id, idCard)


@app.get("/user/see_favourites/", tags=["Your very own favourite cards list"])
async def List_favourite_cards(current_user=Depends(verify_token)):
    """List all the favourite cards of the current user"""
    logging.info("List all the favourite cards of the current user")
    user_id = current_user.user_id
    return card_service.list_favourite_cards(user_id)


@app.delete("/user/delete_favourite/{idCard}", tags=["Your very own favourite cards list"])
async def Delete_favourite_card(idCard: int, current_user=Depends(verify_token)):
    """Delete the card "idCard" from the list of favourites of the current user"""
    logging.info("Delete the card 'idCard' from the list of favourites of the current user")
    user_id = current_user.user_id
    return card_service.delete_favourite_card(user_id, idCard)


# DATABASE MANAGEMENT :CARDS
# create a card
@app.post("/card/create/cardModel", tags=["Database management : cards"])
async def Create_card(card: cardModel, current_user=Depends(verify_admin)):
    """Creates a card in the Magicsearch database"""
    logging.info("Creates a card in the Magicsearch database")
    return card_service.create_card(card_service.cardModel_to_Card(card))


# update a card
@app.put("/card/update/cardModel", tags=["Database management : cards"])
async def Update_card(card: cardModel, current_user=Depends(verify_admin)):
    """Updates a card in the Magicsearch database"""
    logging.info("Updates a card in the Magicsearch database")
    return card_service.update_card(card_service.cardModel_to_Card(card))


# delete a card
@app.delete("/card/delete/cardModel}", tags=["Database management : cards"])
async def Delete_card(idcard: int, current_user=Depends(verify_admin)):
    """Deletes a card in the Magicsearch database"""
    logging.info("Deletes a card in the Magicsearch database")
    return card_service.delete_card(idcard)


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
@app.delete("/user/{username}", tags=["Database management : user"])
async def delete_user(username: str, current_user=Depends(verify_admin)):
    """Deleting a user, only for admins."""
    logging.info(f"Attempting to delete user: {username} by {current_user.username}")
    user = user_service.find_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        logging.info("Deleting user in the Magicsearch database")
        deleted = user_service.delete(current_user, username)
        if not deleted:
            raise HTTPException(status_code=500, detail="Failed to delete user")
        logging.info(f"User {username} successfully deleted.")
        return {"message": f"User {username} deleted successfully."}
    except Exception as e:
        logging.error(f"Error during deletion: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# get a user by their id
@app.get("/user/{user_id}", tags=["Database management : user"])
async def user_by_id(user_id: int, current_user=Depends(verify_admin)):
    """Finds a user based on their id """
    logging.info(
        f"User with id {user_id} requested by {getattr(current_user, 'username', current_user)}"
        )
    user = user_service.find_by_id(user_id, current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# update user
@app.put("/user/{id_user}", tags=["Database management : user"])
def update_user(
    id_user: int,
    j: userModel,
    current_user=Depends(verify_token)
):
    """Updating a user securely (self-update or admin)"""
    logging.info(f"Updating of user {id_user}")

    # Autoriser self-update OU admin
    if current_user.user_id != id_user and not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this user"
        )

    updated_user = user_service.update_user(id_user, j.username, j.password)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")

    return {"message": f"user {updated_user.username} updated successfully"}


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
# async def hello_name(name: str):
#    """Afficher Hello"""
#    logging.info(f"Afficher Hello {name}")
#    return f"message : Hello {name}"

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
