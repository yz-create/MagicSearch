from service.card_service import CardService
from dao.card_dao import CardDao
from business_object.filters.filter_category import FilterCategory
from business_object.filters.filter_numerical import FilterNumeric

cardservice = CardService()
carddao = CardDao()
cat_filter = FilterCategory(
    variable_filtered="type",
    type_of_filtering="positive",
    filtering_value="Legendary Creature - Halfling Scout"
)
num_filter_lower= FilterNumeric(
    variable_filtered="edhrecRank",
    type_of_filtering="lower_than",
    filtering_value=4
)
num_filter_higher= FilterNumeric(
    variable_filtered="edhrecRank",
    type_of_filtering="higher_than",
    filtering_value=2
)
filtertestlist=[num_filter_lower, num_filter_higher]


print(cardservice.filter_search(filtertestlist))