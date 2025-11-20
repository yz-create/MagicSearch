from business_object.card import Card
from dao.card_dao import CardDao
from business_object.filter import Filter

from dotenv import load_dotenv
import random
import psycopg
import logging
from pgvector.psycopg import register_vector
import os
import numpy as np
from utils.embed import embedding
from typing import List


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

    def delete_card(self, id_card: int) -> bool | None:
        """
        Deletes a card from the database.
        Returns True if successful, None if input is invalid or DB fails.
        """
        if not isinstance(id_card, int):
            print("Invalid input: id_card must be the id of the card you want to delete.")
            return None

        try:
            return CardDao().delete_card(id_card)
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
            max_id = CardDao().get_highest_id()
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

    def name_search(self, name: str) -> list[Card]:
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
        """
        Given a search as a sentence (for example "Blue bird with 5 mana"), returns the 5 closest
        cards to the reasearch

        Parameters:
        -----------
        search: str
            The research the user made as an str

        Returns:
        --------
        list[Card]
            The 5 closest cards to match the description made by the user
        """
        search_emb = np.array(embedding(search))

        cards = []
        for entry in CardDao().get_similar_entries(conn, search_emb, False):
            cards.append(CardService().id_search(entry[0]))

        return (cards)

    def semantic_search_shortEmbed(self, search: str) -> list[Card]:
        """
        Given a search as a sentence (for example "Blue bird with 5 mana"), returns the 5 closest
        cards to the reasearch

        Parameters:
        -----------
        search: str
            The research the user made as an str

        Returns:
        --------
        list[Card]
            The 5 closest cards to match the description made by the user
        """
        search_emb = np.array(embedding(search))

        cards = []
        for entry in CardDao().get_similar_entries(conn, search_emb, True):
            cards.append(CardService().id_search(entry[0]))

        return (cards)

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

    def filter_search(self, filters: list[Filter], page: int = 1) -> dict:
        """
        Service method for searching by filtering : checks if it is a valid filter and if it is,
        calls the filtering DAO method for each filter un the list and only keeps the cards common
        to the different filtering. The process is paged meaning that cards 
        are returned 50 at a time.

        Parameters :
        ------------
        filters : list[Filter]
            the list of filters we want to apply to our research
        page : int 
            starts at 1
        page_size : int
            number of cards per page

        Return :
        --------
        dict
            returns 'count' the number of result for filters, 'page' the page you are on, 
            'total_pages' the number of pages of result and 
            'cards' the 50 cards of this page that match the filters
        """
        try:
            if not isinstance(page, int):
                raise TypeError("'page' must be an integer")
            # we check if the filters are valid
            for filter in filters:
                variable_filtered = filter.variable_filtered
                type_of_filtering = filter.type_of_filtering
                filtering_value = filter.filtering_value

                if type_of_filtering in ["positive", "negative"]:  # categorical filter
                    if variable_filtered not in ["type", "color"]:
                        raise ValueError(
                            "variable_filtered must be in the following list : 'type', 'color'")
                    if not isinstance(filtering_value, str):
                        raise TypeError(
                            "filtering_value must be a string")

                if type_of_filtering in [
                    "higher_than", "lower_than", "equal_to"
                ]:  # numerical filter
                    if variable_filtered not in [
                        "manaValue", "defense", "edhrecRank", "toughness", "power", "type"
                    ]:
                        raise ValueError(
                            "variable_filtered must be in the following list :'manaValue', "
                            "'defense', 'edhrecRank', 'toughness', 'power'"
                        )

                if type_of_filtering not in [
                    "higher_than", "lower_than", "equal_to", "positive", "negative"
                ]:
                    raise ValueError(
                        "This is not a filter : type_of_filtering can only take "
                        "'higher_than', 'lower_than', 'equal_to', 'positive' or 'negative' as input"
                        )
                if not filters:
                    logging.warning("Empty filters list")
                    return {"count": 0, "page": page, "total_pages": 0, "cards": []}
                   
            # we apply each filter and get the card ids corresponding 
            card_ids_sets = []
            for filter in filters:
                ids = CardDao().filter_dao(filter)
                if not ids:  # Si un filtre ne retourne rien, le résultat final est vide
                    logging.warning(f"No results for filter: {filter}")
                    return {"count": 0, "page": page, "total_pages": 0, "cards": []}
                card_ids_sets.append(set(ids))

            common_ids_set = set.intersection(*card_ids_sets)
            common_ids = sorted(list(common_ids_set))
            total_count = len(common_ids)
            total_pages = (total_count + 50 - 1) // 50

            # if there are no cards matching the filters
            if total_count == 0:
                logging.warning("No common results for all filters")
                return {"count": 0, "page": page, "total_pages": 0, "cards": []}
            
            # paging
            start_idx = (page - 1) * 50
            end_idx = start_idx + 50
            page_ids = common_ids[start_idx:end_idx]
            # only getting the cards of the page we're on
            page_cards = []
            for card_id in page_ids:
                card = CardDao().id_search(card_id)
                if card:
                    page_cards.append(card.show_card())
                logging.info(f"Returned {len(page_cards)} cards from {total_count} total")
            return {
                "count": total_count,
                "page": page,
                "total_pages": total_pages,
                "cards": page_cards
            }

        except Exception as e:
            logging.error(f"Error in filter_search: {e}")
            return {"error": str(e), "count": 0, "cards": []}

    def add_favourite_card(self, user_id: int, idCard: int) -> bool:
        """"Check whether the idCard exists and adds it to the list of
        favourite cards of the user corresponding to idUser

        Parameters :
        ------------
        user_id : int
            id of the user calling the method

        idCard : int
            id of the card, that the user wants to add to their favourites

        Return:
        -------
        bool
            True if the card is now in the favourite list, False if it's not
        """
        try:
            card_dao = CardDao()
            if not isinstance(user_id, int):
                raise TypeError("user_id must be an integer")
            if not isinstance(idCard, int):
                raise TypeError("idCard must be an integer")
            # new_favourite = idCard
            add = card_dao.add_favourite_card(user_id, idCard)
            if add == "ADDED":
                print(f"The card '{idCard}' had been added to your favourites!")
                return True
            elif add == "EXISTS":
                print(
                    f"The card '{idCard}' is already in your favourites... "
                    "you really like this one !")
                return True
            else:
                print(f"Error adding the card '{idCard}'. Please try again later.")
                return False
        except Exception as e:
            logging.error(f"The input is not an existing card : {e}")
            return False

    def list_favourite_cards(self, user_id: int) -> List[Card]:
        """list all the card marked as favourite by the user 'user_id'"""
        try:
            card_dao = CardDao()
            if not isinstance(user_id, int):
                raise TypeError("user_id must be an integer")
            return card_dao.list_favourite_cards(user_id)
        except Exception as e:
            logging.error(f"There has been a problem showing the list of favourite cards : {e}")
            return False

    def delete_favourite_card(self, user_id: int, idCard: int) -> bool:
        """Delete a card, from the list of favourites of "user_id" """
        try:
            card_dao = CardDao()
            if not isinstance(user_id, int):
                raise TypeError("user_id must be an integer")
            if not isinstance(idCard, int):
                raise TypeError("idCard must be an integer")
            return card_dao.delete_favourite_card(user_id, idCard)
        except Exception as e:
            logging.error(f"There has been a problem deleting the card from favourites : {e}")
            return False

    def cardModel_to_Card(self, card_model):
        return Card(
            card_model.id_card, card_model.layout, card_model.name, card_model.type_line, None,
            None, card_model.ascii_name, card_model.color_identity, card_model.color_indicator,
            card_model.colors, card_model.converted_mana_cost, card_model.defense,
            card_model.edhrec_rank, card_model.edhrec_saltiness, card_model.face_mana_value,
            card_model.face_name, card_model.first_printing, card_model.foreign_data,
            card_model.hand, card_model.has_alternative_deck_limit, card_model.is_funny,
            card_model.is_funny, card_model.keywords, card_model.leadership_skills,
            card_model.legalities, card_model.life, card_model.loyalty, card_model.mana_cost,
            card_model.mana_value, card_model.power, card_model.printings, card_model.purchase_urls,
            card_model.rulings, card_model.side, card_model.subtypes, card_model.supertypes,
            card_model.text, card_model.toughness, card_model.types
        )
