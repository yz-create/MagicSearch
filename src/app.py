import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from service.user_service import UserService
from utils.log_init import initialiser_logs

app = FastAPI(title="MagicSearch")


initialiser_logs("Webservice")

user_service = UserService()

# route vers la documentation 
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")

# routes utilisateurs : get user et get user id
@app.get("/user/", tags=["Users"])
async def list_all_users():
    """Lister tous les users"""
    logging.info("List all users")
    list_users = user_service.list_all()

    liste_model = []
    for user in list_users:
        liste_model.append(user)

    return liste_model


@app.get("/user/{user_id}", tags=["Users"])
async def user_par_id(user_id: int):
    """Trouver un user à partir de son id"""
    logging.info("Trouver un user à partir de son id")
    return user_service.find_by_id(user_id)


# librairie Pydantic BaseModel
class userModel(BaseModel):
    """
    Définir un modèle Pydantic pour les users
    Modèle Pydantic pour valider et documenter les 
    objets utilisateur reçus en entrée ou envoyés en sortie.
    """

    user_id: int | None = None  # Champ optionnel
    pseudo: str
    mdp: str


# création d'un user 
@app.post("/user/", tags=["Users"])
async def create_user(j: userModel):
    """Créer un user"""
    logging.info("Create user")
    if user_service.pseudo_deja_utilise(j.pseudo):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")

    user = user_service.creer(j.pseudo, j.mdp)
    if not user:
        raise HTTPException(status_code=404, detail="Erreur lors de la création du user")

    return user

# modification d"un user
@app.put("/user/{id_user}", tags=["users"])
def modifier_user(id_user: int, j: userModel):
    """Modifier un user"""
    logging.info(f"Modifier user {id_user}")
    user = user_service.trouver_par_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail="user non trouvé")

    user.pseudo = j.pseudo
    user.mdp = j.mdp
    user = user_service.modifier(user)
    if not user:
        raise HTTPException(status_code=404, detail="Erreur lors de la modification du user")

    return f"user {j.pseudo} modifié"


# suppression d'un user
@app.delete("/user/{id_user}", tags=["users"])
def supprimer_user(id_user: int):
    """Supprimer un user"""
    logging.info(f"Supprimer un user {id_user}")
    user = user_service.trouver_par_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail="user non trouvé")

    user_service.supprimer(user)
    return f"user {user.pseudo} supprimé"


# route simple pour tester l'api
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