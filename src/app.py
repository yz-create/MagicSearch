import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from service.joueur_service import JoueurService
from utils.log_init import initialiser_logs

app = FastAPI(title="MagicSearch")


initialiser_logs("Webservice")

user_service = UserService()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


@app.get("/user/", tags=["Users"])
async def list_all_users():
    """Lister tous les users"""
    logging.info("List all users")
    list_users = user_service.list_all()

    liste_model = []
    for joueur in list_users:
        liste_model.append(user)

    return liste_model


@app.get("/user/{user_id}", tags=["Users"])
async def joueur_par_id(user_id: int):
    """Trouver un joueur à partir de son id"""
    logging.info("Trouver un joueur à partir de son id")
    return user_service.find_by_id(user_id)


class JoueurModel(BaseModel):
    """Définir un modèle Pydantic pour les Joueurs"""

    user_id: int | None = None  # Champ optionnel
    pseudo: str
    mdp: str


########################################################

@app.post("/user/", tags=["Users"])
async def create_user(j: JoueurModel):
    """Créer un user"""
    logging.info("Create user")
    if user_service.pseudo_deja_utilise(j.pseudo):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")

    joueur = joueur_service.creer(j.pseudo, j.mdp, j.age, j.mail, j.fan_pokemon)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la création du joueur")

    return joueur


@app.put("/joueur/{id_joueur}", tags=["Joueurs"])
def modifier_joueur(id_joueur: int, j: JoueurModel):
    """Modifier un joueur"""
    logging.info("Modifier un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur.pseudo = j.pseudo
    joueur.mdp = j.mdp
    joueur.age = j.age
    joueur.mail = j.mail
    joueur.fan_pokemon = j.fan_pokemon
    joueur = joueur_service.modifier(joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la modification du joueur")

    return f"Joueur {j.pseudo} modifié"


@app.delete("/joueur/{id_joueur}", tags=["Joueurs"])
def supprimer_joueur(id_joueur: int):
    """Supprimer un joueur"""
    logging.info("Supprimer un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur_service.supprimer(joueur)
    return f"Joueur {joueur.pseudo} supprimé"


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Afficher Hello"""
    logging.info("Afficher Hello")
    return f"message : Hello {name}"


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")