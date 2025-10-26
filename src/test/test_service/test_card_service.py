import re
import pytest
from src.service.card_service import filter_cat_service, filter_num_service


# input test on filter_cat_service
@pytest.mark.parametrize(
    "params, error, error_message",
    [
        (
            {"variable_filtered": "toughness", 
             "type_of_filtering": "positive", 
             "filtering_value": "Legendary Creature - Halfling Scout"},
            ValueError,
            "variable_filtered must be in the following list : "
        ),
        (
            {"variable_filtered": "type", 
             "type_of_filtering": "random", 
             "filtering_value": "Legendary Creature - Halfling Scout"},
            ValueError,
            "type_of_filtering can only take 'positive' or 'negative' as input"
        ),
        (
            {"variable_filtered": "type", 
             "type_of_filtering": "positive", 
             "filtering_value": 9},
            TypeError,
            "filtering_value must be a string"

        )
    ]
)
def test_filter_cat_service_input(params, error, error_message):
    with pytest.raises(error, match=re.escape(error_message)):
        filter_cat_service(**params)


# input test on filter_num_service
@pytest.mark.parametrize(
    "params, error, error_message",
    [
        (
            {"variable_filtered": "type", "type_of_filtering": "equal_to", "filtering_value": 9},
            ValueError,
            "variable_filtered must be in the following list : "
        ),
        (
            {"variable_filtered": "power", "type_of_filtering": "positive", "filtering_value": 9},
            ValueError,
            "type_of_filtering can only take 'higher_than', 'lower_than' or 'equal_to' as input"
        )
    ]
)
def test_filter_num_service_input(params, error, error_message):
    with pytest.raises(error, match=re.escape(error_message)):
        filter_num_service(**params)
