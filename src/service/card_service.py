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
    
    def create_card(self, card: Card) -> bool | None:
        """
        Creates a card in the database.
        Returns True if successful, None if input is invalid or DB fails.
        """
        if not isinstance(card, Card):
            print("Invalid input: must be a Card instance.")
            return None

        try:
            return CardDao().create_card(card)
        except Exception as e:
            print(f"Failed to create card in DB: {e}")
            return None

    def update_card(self, card: Card) -> bool | None:
        """
        Updates a card in the database.
        Returns True if successful, None if input is invalid or DB fails.
        """
        if not isinstance(card, Card):
            print("Invalid input: must be a Card instance.")
            return None

        try:
            return CardDao().update_card(card)
        except Exception as e:
            print(f"Failed to update card in DB: {e}")
            return None

    def delete_card(self, card: Card) -> bool | None:
        """
        Deletes a card from the database.
        Returns True if successful, None if input is invalid or DB fails.
        """
        if not isinstance(card, Card):
            print("Invalid input: must be a Card instance.")
            return None

        try:
            return CardDao().delete_card(card)
        except Exception as e:
            print(f"Failed to delete card from DB: {e}")
            return None

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
        if not isinstance(id, int):
            print("Invalid id type: must be an integer.")
            return None

        if id < 0:
            print("Invalid id: must be non-negative.")
            return None

        try:
            max_id = CardDao().get_higher_id()
        except Exception as e:
            print(f"Failed to get maximum id from DB: {e}")
            return None

        if id > max_id:
            print(f"Invalid id: must not exceed {max_id}.")
            return None

        try:
            card = CardDao().id_search(id)
            return card
        except Exception as e:
            print(f"Failed to fetch card from DB: {e}")
            return None

    def name_search(self, name: str) -> Card:
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
        if not isinstance(name, str):
            print("Invalid name type: must be a string.")
            return None

        if not name.strip():
            print("Invalid name: cannot be empty or whitespace.")
            return None

        try:
            card = CardDao().name_search(name)
            return card
        except Exception as e:
            print(f"Failed to fetch card from DB: {e}")
            return None

    def semantic_search(self, search: str) -> list[Card]:

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
                    "idCard",
                    "embed",
                    search_emb <-> %s as dst
                FROM Card
                ORDER BY dst
                LIMIT 5
                """, (search_emb,))
            return results.fetchall()

        return get_similar_entries(search_emb)

    def view_random_card(self) -> Card:
        """
        Allows to show a random card

        Returns:
        --------
        Card
            The random card obtained
        """
        idmax = CardDao().get_highest_id()
        idrand = random.randint(0, idmax)

        return self.id_search(idrand)

    def filter_search(self, filters: list[AbstractFilter]) -> list[Card]: 
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
        filter = filters[0]
        Magicsearch_filtered = CardDao().filter_dao(filter)
        # we do the same for all the filters and everytime, we only keep in magicsearch_filtered only the common cards
        if len(filters)>=2:
            for i in range(1, len(filters)): # checker que je parcours toute la liste (lucile)
                filter = filters[i]
                new_filter_list = CardDao().filter_dao(filter)
                for item in set(new_filter_list):
                    if item not in set(Magicsearch_filtered):
                        Magicsearch_filtered.remove(item)
        return Magicsearch_filtered or []   
        if not Magicsearch_filtered:
           logging.warning(f"No results for filters: {filters}")
    