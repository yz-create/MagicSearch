from service.card_service import CardService
from dao.card_dao import CardDao
from business_object.filters.filter_category import FilterCategory
from business_object.filters.filter_numerical import FilterNumeric

cardservice = CardService()
carddao = CardDao()
type_filter = FilterCategory(
    variable_filtered="type",
    type_of_filtering="positive",
    filtering_value="Enchantment"
)
color_filterR = FilterCategory(
    variable_filtered="color",
    type_of_filtering="positive",
    filtering_value="R"
)
color_filterB = FilterCategory(
    variable_filtered="color",
    type_of_filtering="positive",
    filtering_value="B"
)
edhrec_filter_lower= FilterNumeric(
    variable_filtered="edhrecRank",
    type_of_filtering="equal_to",
    filtering_value=27784
)
mana_filter= FilterNumeric(
    variable_filtered="manaValue",
    type_of_filtering="equal_to",
    filtering_value=6
)
power_filter= FilterNumeric(
    variable_filtered="power",
    type_of_filtering="equal_to",
    filtering_value=1
)
toughness_filter= FilterNumeric(
    variable_filtered="toughness",
    type_of_filtering="equal_to",
    filtering_value=1
)
# print(carddao.filter_dao(cat2_filter))
filtertestlist=[color_filterB, color_filterR]



print(cardservice.filter_search(filtertestlist))
