from business_object.filters.abstract_filter import AbstractFilter
from business_object.card import Card

class FilterNumeric(AbstractFilter):

    _TYPE_NAME = "filter_num"

    def filter(self, variable_filtered: str, type_of_filtering: str, filtering_value) -> Card:
        """ Filters the magic TG database along a numerical variable
        The filter is applied along a numerical variable defined using the "variable_filtered" and
        a certain criterion depending on the "type_of_filtering" and the "filtering_value"

        Parameters
        ----------
        variable_filtered :
            (this parameter is not defined with an int type because the variables toughness and
            power have some str values
            despite being numerical variables)
            is a numerical variable chosen among the following : manaValue, defense, edhrecRank, toughness, power
        type_of_filtering: str
            defines the way we want to filter the variable. It can only take "higher_than",
            "lower_than" or "equal_to" as input

            higher_than meaning that the filter will select all cards with a value in the
            variable_filtered higher than the filtering_value
            lower_than meaning that the filter will select all cards with a value in the
            variable_filtered lower than the filtering_value
            equal_to meaning that the filter will select all cards with a value in the
            variable_filtered equal to the filtering_value

        filtering_value: str
            is the value (corresponding to the variable_filtered) we want to filter our database
            along

        returns
        -------
            Card : all the cards that fit the chosen criteria
        """
        return
