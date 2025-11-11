import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import re
import pytest
from service.card_service import CardService
from business_object.filters.filter_category import FilterCategory
from business_object.filters.filter_numerical import FilterNumeric



# input test on filter_search
@pytest.mark.parametrize(
    "param"
    [
        
            [FilterNumeric(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ),FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            ), FilterNumeric(
                variable_filtered="edhrecRank",
                type_of_filtering="Answer to the Ultimate Question of Life, the Universe, and Everything",
                filtering_value=27784
            ), FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )],
            [FilterNumeric(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ), FilterCategory(
                variable_filtered="is_funny",
                type_of_filtering="positive",
                filtering_value="B"
            ), FilterNumeric(
                variable_filtered="edhrecRank",
                type_of_filtering="higher_than",
                filtering_value=27784
            ), FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )],
            [FilterNumeric(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ),FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value=42
            ), FilterNumeric(
                variable_filtered="edhrecRank",
                type_of_filtering="higher_than",
                filtering_value=27784
            ), FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )],
            [FilterNumeric(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ),FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value='B'
            ), FilterNumeric(
                variable_filtered="Answer to the Ultimate Question of Life, the Universe, and Everything",
                type_of_filtering="higher_than",
                filtering_value=27784
            ), FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )]
        
    ]
)
def test_filter_search_service_input(param):
    cardservice=CardService()
    assert cardservice.filter_search(param) is False

# faire test sur cumul des filtres
