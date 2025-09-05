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
    login : Se connecter
    menu_joueur : Menu Joueur
    logon : Créer un compte
    player_list : Lister les joueurs
    poke_list : Lister les pokemons
    logout : Se déconnecter

    [*] --> Accueil

    Accueil --> login
    login --> menu_joueur

    Accueil --> logon

    Accueil --> quitter
    quitter --> [*]

    state menu_joueur {
    	[*] --> player_list
    	[*] --> poke_list
    	[*] --> logout
        logout --> [*]:retour accueil
    }
```
