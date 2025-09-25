
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

        + show_card() : str
        + get_embedded() : list[float]
    }

    class CardDAO{
        + id_search(int) : Card
        + name_search(str) : Card
        + create_card(Card) : bool
        + update_card(Card) : bool
        + delete_card(Card) : bool
        + find_all_embedding() : list[float]
        + find_all() : list[Card]
    }

    class CardService{
        + id_search(int) : Card
        + name_search(str) : Card
        + semantic_search(str) : list[Card]
        + view_random_card() : Card  

        + filtered_search(list[AbstractFilter]) : list[Card]
        + exclude_specific_cards_fo3b() : bool
        + search_using_thematic_description() : list[Card]
    }

    class AbstractFilter{
        # raw_name : str
        + add_raw_name(str) : bool
        + get_filter() : AbstractFilter
        
    }

    class FilterNum{
        - value_num : float
        + add_value_num(float) : bool
        + add_filter(nom_colonne, value_num) : bool
    }

    class FilterCategory{
        - value_cat : str
        + add_value_num(str) : FilterCat
        + add_filter(nom_colonne, value_cat) : Filter

    }

    class AbstractUser{
        + user_id : int
        + user_name : str 
    }

    class User{}
    class Admin{}

    class UserDAO {
        + add_user(AbstractUser) : bool
        + delete_user(AbstractUser) : bool
        + add_fav(AbstractUser, Card) : bool
        + delete_fav(AbstractUser, Card) : bool
        + read_all_user(AbstractUser) : bool
        + read_all_fav(AbstractUser) : bool
    }

    class UserService {
        + add_user(str) : bool
        + delete_user(str) : bool
        + add_fav(AbstractUser, Card) : bool
        + delete_fav(AbstractUser, Card) : bool
        + read_all_user(AbstractUser) : bool
        + read_all_fav(AbstractUser) : bool
        + login(str): User
    }

    class DBConnection{
        -__connection : Connection
        +connection() : Connection
    }

    
    CardDAO "1" --> "0..*" Card : create/find/update
    CardService ..> CardDAO : use
    CardService "1" --> "0..*" Card : handle
    CardService "1" --> "0..*" AbstractFilter : use

    AbstractFilter <|-- FilterCategory
    AbstractFilter <|-- FilterNum

    AbstractUser <|-- User
    AbstractUser <|-- Admin
    UserDAO --> AbstractUser : create/find/update
    UserDAO "1" --> "0..*" Card : create/find/update favorites
    UserService ..> UserDAO : use
    UserService "1" --> "0..*" AbstractUser : handle
    UserService "1" --> "0..*" Card : add to favorites
    
    UserDAO ..> DBConnection : use to connect the database
    CardDAO ..> DBConnection : use to connect the database
    
    UserDAO ..> DBConnection : use to connect the database
    CardDAO ..> DBConnection : use to connect the database
```
