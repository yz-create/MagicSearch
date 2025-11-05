from src.service.card_service import CardService
from src.dao.card_dao import CardDao

cardservice = CardService()
carddao = CardDao()
name = '"Ach! Hans, Run!"'

#print(CardDao().name_search(name))
print(cardservice.id_search(1))

#print(cardservice.view_random_card())
