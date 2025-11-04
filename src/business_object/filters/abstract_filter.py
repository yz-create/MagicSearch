from abc import ABC, abstractmethod
from business_object.card import Card


class AbstractFilter(ABC):
    def __init__(self, variable_filtered: str, type_of_filtering: str, filtering_value):
        # pas encore de type à filtering_value parce que peut être catégorie ou nombre
        self.variable_filtered = variable_filtered
        self.type_of_filtering = type_of_filtering
        self.filtering_value = filtering_value

    @abstractmethod
    def filter(self, variable_filtered: str, type_of_filtering: str, filtering_value) -> Card:
        # est ce que ça renvoie une liste ? c'est pas mon problème
        """
        Filters the magic TG database along the variable_filtered, by choosing the cards
        that fit a certain criterion depending on the "type_of_filtering" and the "filtering_value"

        Returns:
            list : the list of all the cards that fit the chosen criteria
        """
        pass

# potentielle nécessité de faire une méthode str si on ajoute les filtres les uns aux autres ??
