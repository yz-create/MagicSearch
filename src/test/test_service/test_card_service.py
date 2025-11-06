import re
import pytest
from src.service.card_service import filter_cat_service, filter_num_service
from business_object.filters.filter_category import FilterCategory
from business_object.filters.filter_numerical import FilterNumeric


# input test on filter_cat_service
@pytest.mark.parametrize(
    "params, error, error_message",
    [
        (
            {[FilterNumeric(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ),FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            ), FilterNumeric(
                variable_filtered="edhrecRank",
                type_of_filtering="blablabla",
                filtering_value=27784
            ), FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )]},
            ValueError("This is not a filter : type_of_filtering can only take "
                    "'higher_than', 'lower_than', 'equal_to', 'positive' or 'negative' as input ")
        ),
        (
            {[FilterNumeric(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ),FilterCategory(
                variable_filtered="is_funny",
                type_of_filtering="positive",
                filtering_value="B"
            ), FilterNumeric(
                variable_filtered="edhrecRank",
                type_of_filtering="blablabla",
                filtering_value=27784
            ), FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )]}, 
            ValueError("variable_filtered must be in the following list : 'type', 'color'")
        ),
        (
            {[FilterNumeric(
                variable_filtered="toughness",
                type_of_filtering="equal_to",
                filtering_value=1
            ),FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value=42
            ), FilterNumeric(
                variable_filtered="edhrecRank",
                type_of_filtering="blablabla",
                filtering_value=27784
            ), FilterCategory(
                variable_filtered="color",
                type_of_filtering="positive",
                filtering_value="B"
            )]},
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
            "variable_filtered must be in the following list : manaValue, defense, edhrecRank, toughness, power"
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


