# Diagramme d'activité

> Un diagramme UML d'activité modélise le flux de travail d'un processus, montrant la séquence d'activités et de décisions dans un système. Il illustre comment les actions s'enchaînent et comment les choix sont faits.

Ce diagramme est codé avec [mermaid](https://mermaid.js.org/syntax/stateDiagram.html) :

- avantage : facile à coder
- inconvénient : on ne maîtrise pas bien l'affichage

Pour afficher ce diagramme dans VScode :

- à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
- rechercher `mermaid`
  - installer l'extension **Markdown Preview Mermaid Support**
- revenir sur ce fichier
  - faire **CTRL + K**, puis **V**


```mermaid
stateDiagram
    menu_joueur : Player menu
    search_card : Search a card
    search_card_name : Search a card with its name or number
    semantic_search : Semantic search
    radom_card : View a random card
    proposition: Proposition de carte ressemblant
    semantic_search_description  :Saisir une description peu précise
    login : Se connecter
    logon : Créer un compte

    logout : Se déconnecter

    [*] --> Accueil

    Accueil --> login
    login --> menu_joueur

    Accueil --> logon

    Accueil --> quitter
    quitter --> [*]






    state menu_joueur {
        [*] --> search_card
    	search_card --> search_card_name
        search_card --> radom_card
    	search_card --> semantic_search
    	[*] --> logout




        search_card_name --> proposition: saisie invalide
        proposition --> search_card

        semantic_search --> semantic_search_description: utiliser des filtres si besoin



        logout --> [*]:retour accueil
    }

```
