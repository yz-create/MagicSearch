import re
import pytest
from service.card_service import filter_cat, filter_num


# 1. vérifier les inputs
# 2. vérifier que des cartes qui ne sont pas censés y être n'y sont pas
# 3. vérifier que des cartes qui sont censés y être y sont

#input test on filter_cat
@pytest.mark.parametrize(
    "params, error, error_message",
    [
        (
            {"variable_filtered": "toughness", "type_of_filtering": "positive", "filtering_value": "halfling scout"},
            ValueError,
            "variable_filtered must be in the following list : "
        ),
        (
            {"variable_filtered": "subtype", "type_of_filtering": "random", "filtering_value": "halfling scout"},
            ValueError,
            "type_of_filtering can only take 'positive' or 'negative' as input"
        ),
        (
            {"variable_filtered": "subtype", "type_of_filtering": "positive", "filtering_value": 9},
            TypeError,
            "filtering_value must be a string"

        )
    ]
)
def test_filter_cat_input(params, error, error_message):
    with pytest.raises(error, match=re.escape(error_message)):
        filter_cat(**params)


#input test on filter_num
@pytest.mark.parametrize(
    "params, error, error_message",
    [
        (
            {"variable_filtered": "type", "type_of_filtering": "equal_to", "filtering_value": 9},
            ValueError,
            "variable_filtered must be in the following list : "
        ),
        (
            {"variable_filtered": "power", "type_of_filtering": "positive", "filtering_value":9},
            ValueError,
            "type_of_filtering can only take 'higher_than', 'lower_than' or 'equal_to' as input"
        )
    ]
)
def test_filter_num_input(params, error, error_message):
    with pytest.raises(error, match=re.escape(error_message)):
        filter_num(**params)


# test 