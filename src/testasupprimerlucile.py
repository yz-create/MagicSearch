from service.card_service import CardService
from dao.card_dao import CardDao
from business_object.filter import Filter

cardservice = CardService()
carddao = CardDao()
type_filter = Filter(
    variable_filtered="type",
    type_of_filtering="positive",
    filtering_value="Enchantment"
)
color_filterW = Filter(
    variable_filtered="color",
    type_of_filtering="positive",
    filtering_value="W"
)
color_filterB = Filter(
    variable_filtered="color",
    type_of_filtering="positive",
    filtering_value="B"
)
edhrec_filter_lower= Filter(
    variable_filtered="edhrecRank",
    type_of_filtering="equal_to",
    filtering_value=27784
)
mana_filter= Filter(
    variable_filtered="manaValue",
    type_of_filtering="equal_to",
    filtering_value=6
)
power_filter= Filter(
    variable_filtered="power",
    type_of_filtering="equal_to",
    filtering_value=1
)
toughness_filter= Filter(
    variable_filtered="toughness",
    type_of_filtering="equal_to",
    filtering_value=1
)
#print(carddao.filter_dao(type_filter))
filtertestlist=[toughness_filter, mana_filter, color_filterB]


print(cardservice.filter_search(filtertestlist))
#print(cardservice.list_favourite_cards("caramba"))

