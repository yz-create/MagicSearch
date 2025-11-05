from business_object.card import Card
from dao.card_dao import CardDao
from business_object.filters.abstract_filter import AbstractFilter

from dotenv import load_dotenv
import random
import psycopg
from pgvector.psycopg import register_vector
import requests
import os

# Set the following env. variables for this to work: PGUSER, PGPASSWORD, PGHOST, PGPORT, PGDATABASE
# conn = psycopg.connect(dbname="defaultdb", autocommit=True)
load_dotenv()

conn = psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DATABASE"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    autocommit=True
)
register_vector(conn)


class CardService():
    """Class containing the service methods of Cards"""
    
    def create_card(self, card:  Card) -> bool:
        # peut être lever des erreur si on veut pas de doublons, meme si je crois que des erreurs sont levées dans DAO  (lucile)
        return self.CardDao().create_card(card)

    def update_card(self, card: Card)-> bool : 
        return self.CardDao().update_card(card)
    
    def delete_card(self, card) :
        return self.CardDao().delete_card(card)
 
    def id_search(self, id: int) -> Card:
        """
        Searches for a card based on its id

        Parameters:
        ===========
        id: int
            The id of the searched card

        Returns:
        ========
        Card
            The Card with the id given
        """
        try:
            return CardDao().id_search(id)
        except (ValueError, TypeError):
            # id invalid, return None instead of crashing
            return None

    def name_search(name: str) -> Card:
        """
        Searches for a card based on its name

        Parameters:
        ===========
        name: str
            The name of the searched card

        Returns:
        ========
        Card
            The Card with the name given
        """
        return CardDao().name_search(name)

    def semantic_search(search: str) -> list[Card]:

        # étape 1 : obtenir l'embedding de "search"
        token = os.getenv("API_TOKEN")
        url = "https://llm.lab.sspcloud.fr/ollama/api/embed"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-type": "application/json"}

        def embedding(text: str):

            data = {
                "model": "bge-m3:latest",
                "input": text
            }

            response = requests.post(url, headers=headers, json=data)
            json_response = response.json()
            # res = json_response[ "embeddings"]
            return json_response

        search_emb = embedding(search)

        # étape 2 : obtenir la correspondance entre search_emb et au moins 5 de nos cartes

        def get_similar_entries(embedding):
            """
            Returns the 5 entries from the database with the embedding closest to the given
            [search_emb].
            """
            results = conn.execute("""
                SELECT
                    embed,
                    search_emb <-> %s as dst
                FROM Card
                ORDER BY dst
                LIMIT 5
                """, (search_emb,))
            return results.fetchall()

        return get_similar_entries(search_emb)

    def view_random_card() -> Card:
        """
        Allows to show a random card

        Returns:
        --------
        Card
            The random card obtained
        """
        idmax = CardDao.get_highest_id()
        idrand = random.randint(0, idmax)
        CardService.id_search(idrand)

    def filter_search(filters: list[AbstractFilter]) -> list[Card]: 
        """
        Service method for searching by filtering : identifies the type of filter and calls the corresponding DAO
        method

        Parameters :
        ------------
        filters : list[AbstractFilter]
            the list of filters we want to apply to our research

        Return :
        --------
        List[Card]
            The Cards corresponding to our filter
        """
        # we start a basic list with the first filter in our list
        filter=filters[0]
        Magicsearch_filtered = CardDao().filter_dao(filter)
        # we do the same for all the filters and everytime, we only keep in magicsearch_filtered only the common cards
        if len(filters)>=2 :
            for i in range(1,len(filters)-1): # checker que je parcours toute la liste (lucile)
                filter = filters[i]
                new_filter_list = CardDao().filter_dao(filter)
                for item in set(new_filter_list):
                    if item not in set(Magicsearch_filtered):
                        Magicsearch_filtered.remove(item)
        return Magicsearch_filtered       
  