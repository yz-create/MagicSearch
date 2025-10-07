from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.utlisateur import User
from dao.joueur_dao import JoueurDao


class JoueurService:
    """Classe contenant les méthodes de service des Joueurs"""

    @log
    def creer(self, pseudo, mdp) -> User:
        """Création d'un joueur à partir de ses attributs"""

        nouveau_user = User(
            pseudo=pseudo,
            mdp=hash_password(mdp, pseudo)
        )

        return nouveau_user if JoueurDao().creer(nouveau_user) else None

    @log
    def lister_tous(self, inclure_mdp=False) -> list[User]:
        """Lister tous les joueurs
        Si inclure_mdp=True, les mots de passe seront inclus
        Par défaut, tous les mdp des joueurs sont à None
        """
        joueurs = JoueurDao().lister_tous()
        if not inclure_mdp:
            for j in joueurs:
                j.mdp = None
        return joueurs

    @log
    def trouver_par_id(self, id_user) -> User:
        """Trouver un joueur à partir de son id"""
        return JoueurDao().trouver_par_id(id_user)

    @log
    def modifier(self, joueur) -> User:
        """Modification d'un joueur"""

        joueur.mdp = hash_password(joueur.mdp, joueur.pseudo)
        return joueur if JoueurDao().modifier(joueur) else None

    @log
    def supprimer(self, joueur) -> bool:
        """Supprimer le compte d'un joueur"""
        return JoueurDao().supprimer(joueur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les joueurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["pseudo", "age", "mail", "est fan de Pokemon"]

        joueurs = JoueurDao().lister_tous()

        for j in joueurs:
            if j.pseudo == "admin":
                joueurs.remove(j)

        joueurs_as_list = [j.as_list() for j in joueurs]

        str_joueurs = "-" * 100
        str_joueurs += "\nListe des joueurs \n"
        str_joueurs += "-" * 100
        str_joueurs += "\n"
        str_joueurs += tabulate(
            tabular_data=joueurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_joueurs += "\n"

        return str_joueurs

    @log
    def se_connecter(self, pseudo, mdp) -> User:
        """Se connecter à partir de pseudo et mdp"""
        return JoueurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    @log
    def pseudo_deja_utilise(self, pseudo) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        joueurs = JoueurDao().lister_tous()
        return pseudo in [j.pseudo for j in joueurs]
