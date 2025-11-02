from abstract_filter.py import AbstractFilter
from cards import Card


class FilterCategory(AbstractFilter):

    _TYPE_NAME = "filter_cat"

    def filter(self, variable_filtered: str, type_of_filtering: str, filtering_value: str) -> Card:
        """ Filters the magic TG database along a categorical variable
        The filter is applied along a categorical variable defined using the "variable_filtered" and
        a certain criterion depending on the "type_of_filtering" and the "filtering_value"

        Parameters
        ----------
        variable_filtered: str
            is a categorical variable chosen among the following :type

        type_of_filtering: str
            defines the way we want to filter the variable.
            It can only take "positive" or "negative" as an input
            positive meaning that the filter will select all cards
            with a value in the variable_filtered equal to the filtering_value
            negative meaning that the filter will select all cards
            with a value in the variable_filtered different from the filtering_value

        filtering_value: str
            is the value (corresponding to the variable_filtered)
            we want to filter our database along

        returns
        -------
            Card : all the cards that fit the chosen criteria
        """
        return
