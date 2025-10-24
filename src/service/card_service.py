from business_object.card import Card
from dao.card_dao import CardDAO
from business_object.filters.abstract_filter import Abstractfilter


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

    def filter_cat_service(self, filter: Abstractfilter):
        """

        """
        variable_filtered = filter.variable_filtered
        type_of_filtering = filter.type_of_filtering
        filtering_value = filter.filtering_value
        if variable_filtered not in ["type", "subtype"]:
            raise ValueError("variable_filtered must be in the following list : ")
        if type_of_filtering != "positive" & type_of_filtering != "negative":
            raise ValueError("type_of_filtering can only take 'positive' or 'negative' as input")
        if not isinstance(filtering_value, str):
            raise ValueError("filtering_value must be a string")
        return CardDAO().filter_cat_dao(filter)

    def filter_num_service(self, filter: Abstractfilter):
        """
        """
        variable_filtered = filter.variable_filtered
        type_of_filtering = filter.type_of_filtering
        if variable_filtered not in ["power", "toughness"]:
            raise ValueError("variable_filtered must be in the following list : ")
        if type_of_filtering not in ["higher_than", "lower_than", "equal_to"]:
            raise ValueError("type_of_filtering can only take 'higher_than', 'lower_than' or 'equal_to' as input")
        return CardDAO().filter_num_dao(filter)
