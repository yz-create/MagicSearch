from src.service.card_service import CardService
from src.dao.card_dao import CardDao


carddao = CardDao()
name = "Lightning Bolt"

#print(CardDao().name_search(name))
print(CardService().name_search(name))

#print(cardservice.view_random_card())
