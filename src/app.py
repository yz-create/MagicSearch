import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from service.user_service import UserService
from service.card_service import CardService
from utils.log_init import initialize_logs
# from business_object.filters.abstract_filter import AbstractFilter 
# pour les fonctions de filtrages


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
card_service = CardService()


# USER LOG IN 

# librairie Pydantic BaseModel 
class userModel(BaseModel):
    """
    defines a Pydantic model for the users
    Pydantic model to validate and document the user objects 
    received as input and returned as output
    """

    user_id: int | None = None  # Champ optionnel
    pseudo: str
    mdp: str


# creating a user
@app.post("/user/", tags=["User log in !"])
async def create_user(j: userModel):
    """creating a user"""
    logging.info("creating a user")
    if user_service.pseudo_deja_utilise(j.pseudo):
        raise HTTPException(status_code=404, detail="Pseudo already used")

    user = user_service.creer(j.pseudo, j.mdp)
    if not user:
        raise HTTPException(status_code=404, detail="Error while creating the user")

    return user


# ROAMING IN THE MAGICSEARCH DATABASE
# list all cards ?
# get a random card
# Card_Service().view_random_card()
@app.get("/card/", tags=["Roaming in the MagicSearch Database"])
async def view_random():
    """get a random card"""
    logging.info("get a random card")
    return card_service.view_random_card()


# get a card by its id 
# Card_Service().id_search(id)
@app.get("/card/{id}", tags=["Roaming in the MagicSearch Database"])
async def id_search(id: int):
    """Finds a card based on its id """
    logging.info("Finds a card based on its id ")
    return card_service.id_search(id)


# get a card by its name
# Card_Service().name_search(name)
@app.get("/card/{name}", tags=["Roaming in the MagicSearch Database"]) 
async def name_search(name: str):
    """Finds a card based on its name """
    logging.info("Finds a card based on its name")
    return card_service.name_search(name)


# get the result of a semantic search
# Card_Service().semantic_search(search)
@app.get("/card/{search}", tags=["Roaming in the MagicSearch Database"])
async def semantic_search(search):
    """Finds a card based on its a semantic search"""
    logging.info("Finds a card based on its a semantic search")
    return card_service.semantic_search(search)

    
# get a filtered list of cards
# Card_Service().filter_num_service(self, filter: AbstractFilter)
# card_service().filter_cat_service(self, filter: AbstractFilter)
@app.get("/card/{filter}", tags=["Roaming in the MagicSearch Database"]) 
async def filter_numerical(filter):
    """Filters the database based on a numerical criterion"""
    logging.info("Filters the database based on a numerical criterion")
    return card_service.filter_num_service(filter)


@app.get("/card/{filter}", tags=["Roaming in the MagicSearch Database"]) 
async def filter_categorical(filter):
    """Filters the database based on a categorical criterion"""
    logging.info("Filters the database based on a categorical criterion")
    return card_service.filter_cat_service(filter)


# DATABASE MANAGEMENT :CARDS
# create a card
@app.get("/card/{card}", tags=["Database management : cards"]) 
async def Create_card(card):
    """Creates a card in the Magicsearch database"""
    logging.info("Creates a card in the Magicsearch database")
    return card_service.create_card(card)


# update a card
@app.get("/card/{card}", tags=["Database management : cards"]) 
async def Update_card(card):
    """Updates a card in the Magicsearch database"""
    logging.info("Updates a card in the Magicsearch database")
    return card_service.update_card(card)


# delete a card
@app.get("/card/{card}", tags=["Database management : cards"]) 
async def Delete_card(card):
    """Deletes a card in the Magicsearch database"""
    logging.info("Deletes a card in the Magicsearch database")
    return card_service.delete_card(card)


# DATABASE MANAGEMENT : USER
# routes utilisateurs : get user et get user id
# list the users
@app.get("/user/", tags=["Database management : user"])
async def list_all_users():
    """Lister tous les users"""
    logging.info("List all users")
    list_users = user_service.list_all()

    liste_model = []
    for user in list_users:
        liste_model.append(user)

    return liste_model


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

    user.pseudo = j.pseudo
    user.mdp = j.mdp
    user = user_service.modifier(user)
    if not user:
        raise HTTPException(status_code=404, detail="Error while updating user")

    return f"user {j.pseudo} updated"


# deleting a user
@app.delete("/user/{id_user}", tags=["Database management : user"])
def Delete_user(id_user: int):
    """Deleting a user"""
    logging.info(f"Deleting user {id_user}")
    user = user_service.trouver_par_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    user_service.supprimer(user)
    return f"user {user.pseudo} deleted"


# API TEST
@app.get("/hello/{name}")
async def hello_name(name: str):
    """Afficher Hello"""
    logging.info(f"Afficher Hello {name}")
    return f"message : Hello {name}"

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")