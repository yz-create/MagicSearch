from business_object.card import Card
from dao.card_dao import CardDAO


class User_Service():
    """Class containing the service methods of Cards"""

    def id_search(id: int) -> Card:
        """
        Searches for a card based on its id

        Parameters:
        ===========
        id: int
            The id of the searched card

        Returns:
        ========
        Card
            The Card with the id given
        """
        return CardDAO().id_search(id)

    def name_search(name: str) -> Card:
        """
        Searches for a card based on its name

        Parameters:
        ===========
        name: str
            The name of the searched card

        Returns:
        ========
        Card
            The Card with the name given
        """
        return CardDAO().name_search(name)

    def semantic_search(search: str) -> list[Card]:
        pass

    def view_random_card() -> Card:
        pass
