from typing import Union
from business_object.card import Card


class Filter:
    def __init__(self, variable_filtered: str, type_of_filtering: str, filtering_value: Union[int, str]):
        self.variable_filtered = variable_filtered
        self.type_of_filtering = type_of_filtering
        self.filtering_value = filtering_value

    def __str__(self):
        return f"The filter is applied to the column {self.variable_filtered} of the database, it is a {self.type_of_filtering} kind of filter and it filters around {self.filtering_value}"

    def __repr__(self):
        return f"Filter(variable_filtered={self.variable_filtered}, type_of_filtering={self.type_of_filtering}, filtering_value={self.filtering_value})"
