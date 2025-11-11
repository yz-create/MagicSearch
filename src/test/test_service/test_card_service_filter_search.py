import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import re
import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
from service.card_service import CardService
from business_object.filter import Filter



# input test on filter_search
@pytest.mark.parametrize(
    "param",
    [
        
            [ Filter(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ), Filter(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            ),  Filter(
                variable_filtered="edhrecRank",
                type_of_filtering="Answer to the Ultimate Question of Life, the Universe, and Everything",
                filtering_value=27784
            ),  Filter(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )],
            [ Filter(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ),  Filter(
                variable_filtered="is_funny",
                type_of_filtering="positive",
                filtering_value="B"
            ),  Filter(
                variable_filtered="edhrecRank",
                type_of_filtering="higher_than",
                filtering_value=27784
            ),  Filter(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )],
            [ Filter(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ), Filter(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value=42
            ),  Filter(
                variable_filtered="edhrecRank",
                type_of_filtering="higher_than",
                filtering_value=27784
            ),  Filter(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )],
            [ Filter(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ), Filter(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value='B'
            ),  Filter(
                variable_filtered="Answer to the Ultimate Question of Life, the Universe, and Everything",
                type_of_filtering="higher_than",
                filtering_value=27784
            ),  Filter(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )]
        
    ]
)
def test_filter_search_service_input(param):
    cardservice=CardService()
    assert cardservice.filter_search(param) is False


# test whether the filters are added rightly to one another
@pytest.fixture
def mock_filters():
    # Création de deux filtres valides
    filter1 = Filter(variable_filtered="color", type_of_filtering="positive", filtering_value="red")
    filter2 = Filter(variable_filtered="type", type_of_filtering="positive", filtering_value="Creature")
    return [filter1, filter2]

@patch("service.card_service.CardDao")  
def test_filter_search_cumulative(mock_carddao, mock_filters):
    # Simulates two successive calls to Card Dao 
    dao_instance = mock_carddao.return_value
    dao_instance.filter_dao.side_effect = [
        [{"idCard": 1}, {"idCard": 2}, {"idCard": 3}],  # the output of the first filter
        [{"idCard": 2}, {"idCard": 4}]                  # the output of the second one
    ]

    service = CardService()
    result = service.filter_search(mock_filters)

    # checks that filter_dao has been called twice
    assert dao_instance.filter_dao.call_count == 2

    # check that only the common cards are kept 
    assert result == [{"idCard": 2}]