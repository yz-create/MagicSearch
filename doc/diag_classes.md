
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
    class Card {
        # id_card: int
        # name: string
        # embedded: string

        + show_card() :: str
        + get_embedded() :: list[float]
    }

    class CardDAO{
        + id_search(int) :: Card
        + name_search(str) :: Card
        + create_card(Card) :: bool
        + update_card(Card) :: bool
        + delete_card(Card) :: bool
    }

    class CardSevice{
        + id_search(int) :: Card
        + name_search(str) :: Card
        + semantic_search(str) :: list[Card]
        + view_random_card() :: Card  

        + filtered_search(list[AbstractFilter]) :: list[Card]
        + exclude_specific_cards_fo3b()
        + search_using_thematic_description()
    }

    class AbstractFilter{
        # nom_colonne : str
        + add_nom_colonne(str) 
        + get_filter() :: AbstractFilter
        
    }

    class FiltreNum{
        - value_num : float
        + add_value_num(float) 
        + add_filtre(nom_colonne, value_num) 
    }

    class FiltreCategory{
        - value_cat : str
        + add_value_num(str) -> FiltreCat
        + add_filtre(nom_colonne, value_cat) -> Filtre

    }

    class AbstractUser{
        + user_name : str 
        + use_class_card(pseudo)
    }

    class User{}
    class Admin{}

    class UserDAO {
        + add_user(AbstractUser) :: bool
        + delete_user(AbstractUser) :: bool
        + add_fav(AbstractUser, Card) :: bool
        + delete_fav(AbstractUser, Card) :: bool
        + read_all_user(AbstractUser) : bool
        + read_all_fav(AbstractUser) : bool
    }

    class UserService {
        + add_user(str) :: bool
        + delete_user(str) :: bool
        + add_fav(AbstractUser, Card) :: bool
        + delete_fav(AbstractUser, Card) :: bool
        + read_all_user(AbstractUser) : bool
        + read_all_fav(AbstractUser) : bool
        +login(str): User
    }


    

    CardService ..> CardDao : appelle
    Card <.. CardService: utilise
    Card <.. CardDAO: utilise
    AbstractFilter <|-- FiltreCategory
    AbstractFilter <|-- FiltreNum
    CardSevice <.. AbstractFilter: use

    AbstractUser <|-- User
    AbstractUser <|-- Admin
    AbstractUser <.. UserService: utilise
    AbstractUser <.. UserDAO: utilise
    UserService 
```
