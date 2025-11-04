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


class Card_Service():
    """Class containing the service methods of Cards"""

    def id_search(id: int) -> Card:
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
        return CardDao().id_search(id)

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
        Card_Service.id_search(idrand)

    def filter_cat_service(self, filter: AbstractFilter):
        """
        Service method for numerical filtering : raises errors and calls the corresponding DAO
        method

        Parameters :
        ------------
        filter : Abstractfilter
            the filter we want to apply to our research

        Return :
        --------
        Card
            The Cards corresponding to our filter
        """
        variable_filtered = filter.variable_filtered
        type_of_filtering = filter.type_of_filtering
        filtering_value = filter.filtering_value
        if variable_filtered not in ["type"]:
            raise ValueError("variable_filtered must be in the following list : type")
        if type_of_filtering != "positive" & type_of_filtering != "negative":
            raise ValueError("type_of_filtering can only take 'positive' or 'negative' as input")
        if not isinstance(filtering_value, str):
            raise ValueError("filtering_value must be a string")
        return CardDao().filter_cat_dao(filter)

    def filter_num_service(self, filter: AbstractFilter):
        """
        Service method for numerical filtering : raises errors and calls the corresponding DAO
        method

        Parameters :
        ------------
        filter : Abstractfilter
            the filter we want to apply to our research

        Return :
        --------
        Card
            The Cards corresponding to our filter
        """
        variable_filtered = filter.variable_filtered
        type_of_filtering = filter.type_of_filtering
        if variable_filtered not in ["manaValue", "defense", "edhrecRank", "toughness", "power"]:
            raise ValueError("variable_filtered must be in the following list : manaValue, defense, edhrecRank, toughness, power")
        if type_of_filtering not in ["higher_than", "lower_than", "equal_to"]:
            raise ValueError("type_of_filtering can only take 'higher_than', 'lower_than' or 'equal_to' as input")
        return CardDao().filter_num_dao(filter)
