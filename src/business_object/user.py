class User:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    id_utilisateur : int
        identifiant
    pseudo : str
        pseudo du joueur
    mdp : str
        le mot de passe du joueur
    
    """

    def __init__(self, pseudo, mdp=None, id_user=None):
        """Constructeur"""
        self.id_user = id_user
        self.pseudo = pseudo
        self.mdp = mdp

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"User({self.pseudo})"

    def as_list(self) -> list[str]:
        """Retourne les attributs du joueur dans une liste"""
        return [self.pseudo, self.age]
