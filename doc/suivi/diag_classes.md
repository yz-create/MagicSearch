
# Diagramme de classes des objets métiers

Ce diagramme est codé avec [mermaid](https://mermaid.js.org/syntax/classDiagram.html) :

* avantage : facile à coder
* inconvénient : on ne maîtrise pas bien l'affichage

Pour afficher ce diagramme dans VScode :

* à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
* rechercher `mermaid`
  * installer l'extension **Markdown Preview Mermaid Support**
* revenir sur ce fichier
  * faire **CTRL + K**, puis **V**

```mermaid
classDiagram
    class Joueur {
        +id_joueur: int
        +pseudo: string
        +mdp: string
        +age: int
        +mail: string
        +fan_pokemon: bool
    }

    class JoueurDao {
        +creer(Joueur): bool
        +trouver_par_id(int): Joueur
        +lister_tous(): list[Joueur]
        +supprimer(Joueur): bool
        +se_connecter(str,str): Joueur
    }

    class JoueurService {
        +creer(str...): Joueur
        +trouver_par_id(int): Joueur
        +lister_tous(): list[Joueur]
        +afficher_tous(): str
        +supprimer(Joueur): bool
        +se_connecter(str,str): Joueur
    }

    class AccueilVue {
    }

    class ConnexionVue {
    }

    class MenuJoueurVue {
    }

    class VueAbstraite{
      +afficher()
      +choisir_menu()
    }

    VueAbstraite <|-- AccueilVue
    VueAbstraite <|-- ConnexionVue
    VueAbstraite <|-- MenuJoueurVue
    MenuJoueurVue ..> JoueurService : appelle
    ConnexionVue ..> JoueurService : appelle
    JoueurService ..> JoueurDao : appelle
    Joueur <.. JoueurService: utilise
    Joueur <.. JoueurDao: utilise
```
