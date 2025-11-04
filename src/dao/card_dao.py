import logging

from business_object.card import Card
from db_connection import DBConnection
from business_object.filters.abstract_filter import AbstractFilter


class CardDao:
    # Pattern Singleton : empêche la création de plusieurs objets,
    # renvoie toujours la même instance existante

    def create_card(card: Card) -> bool:
        """
        Add a card to the database
        """
        pass

    def create_card(self, card: Card) -> bool:
        """
        Add a card to the database

        Parameters
        ----------
        card : Card
            The card to add

        Returns
        -------
        bool
            True if creation succeeded, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO "Card" (
                            "layout", "name", "type", "text_to_embed", "embed",
                            "asciiName", "convertedManaCost", "defense", "edhrecRank",
                            "edhrecSaltiness", "faceManaValue", "faceName", "firstPrinting",
                            "hand", "hasAlternativeDeckLimit", "isFunny", "isReserved",
                            "leadershipSkills", "legalities", "life", "loyalty", "manaCost",
                            "manaValue", "power", "side", "text", "toughness"
                        ) VALUES (
                            %(layout)s, %(name)s, %(type)s, %(text_to_embed)s, %(embed)s,
                            %(asciiName)s, %(convertedManaCost)s, %(defense)s, %(edhrecRank)s,
                            %(edhrecSaltiness)s, %(faceManaValue)s, %(faceName)s, 
                            %(firstPrinting)s, %(hand)s, %(hasAlternativeDeckLimit)s, 
                            %(isFunny)s, %(isReserved)s, %(leadershipSkills)s, 
                            %(legalities)s, %(life)s, %(loyalty)s, %(manaCost)s,
                            %(manaValue)s, %(power)s, %(side)s, %(text)s, %(toughness)s
                        ) RETURNING "idCard";
                        """,
                        {
                            "layout": card.layout,
                            "name": card.name,
                            "type": card.type_line,
                            "text_to_embed": card.text or "",
                            "embed": card.get_embedded() or [],
                            "asciiName": card.ascii_name,
                            "convertedManaCost": card.converted_mana_cost,
                            "defense": card.defense,
                            "edhrecRank": card.edhrec_rank,
                            "edhrecSaltiness": card.edhrec_saltiness,
                            "faceManaValue": card.face_mana_value,
                            "faceName": card.face_name,
                            "firstPrinting": card.first_printing,
                            "hand": card.hand,
                            "hasAlternativeDeckLimit": card.has_alternative_deck_limit,
                            "isFunny": card.is_funny,
                            "isReserved": card.is_reserved,
                            "leadershipSkills": None,  # À gérer séparément
                            "legalities": None,  # À gérer séparément
                            "life": card.life,
                            "loyalty": card.loyalty,
                            "manaCost": card.mana_cost,
                            "manaValue": card.mana_value,
                            "power": card.power,
                            "side": None,
                            "text": card.text,
                            "toughness": card.toughness
                        }
                    )
                    result = cursor.fetchone()
                    return result is not None
        except Exception as e:
            logging.error(f"Error creating card: {e}")
            return False

    def update_card(self, card: Card) -> bool:
        """
        Update an existing card in the database

        Parameters
        ----------
        card : Card
            The card with updated information

        Returns
        -------
        bool
            True if update succeeded, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE "Card" SET
                            "name" = %(name)s,
                            "text" = %(text)s,
                            "manaCost" = %(manaCost)s,
                            "manaValue" = %(manaValue)s,
                            "power" = %(power)s,
                            "toughness" = %(toughness)s,
                            "text_to_embed" = %(text_to_embed)s,
                            "embed" = %(embed)s
                        WHERE "idCard" = %(idCard)s;
                        """,
                        {
                            "idCard": card.ascii_name,  # Besoin d'un ID dans Card
                            "name": card.name,
                            "text": card.text,
                            "manaCost": card.mana_cost,
                            "manaValue": card.mana_value,
                            "power": card.power,
                            "toughness": card.toughness,
                            "text_to_embed": card.text or "",
                            "embed": card.get_embedded() or []
                        }
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error updating card: {e}")
            return False
    
    def delete_card(self, card_id: int) -> bool:
        """
        Delete a card from the database

        Parameters
        ----------
        card_id : int
            ID of the card to delete

        Returns
        -------
        bool
            True if deletion succeeded, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'DELETE FROM "Card" WHERE "idCard" = %(idCard)s;',
                        {"idCard": card_id}
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error deleting card: {e}")
            return False
    
    def find_all_embedding(self, limit: int = 100, offset: int = 0) -> list[float]:
        request = (
            f"SELECT embedded                                                  "
            f"  FROM AtomicCards                                                  "
            # f"  JOIN tp.pokemon_type pt ON pt.id_pokemon_type = p.id_pokemon_type    "
            f" LIMIT {max(limit, 0)}                                                 "
            f"OFFSET {max(offset, 0)}                                                "
        )

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(request)
                res = cursor.fetchall()

        embedding = []

        for row in res:
            embedding.append(row)
        return embedding
        
    def find_by_embedding(self, limit: int = 100, offset: int = 0) -> list[float]:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                                                        "
                    "  FROM AtomicCards c                                            "
                    # "  JOIN tp.pokemon_type pt USING(id_pokemon_type)                "
                    " WHERE c.name = %(name)s                                        ",
                    {"name": name},
            )
            res = cursor.fetchone()

        embedding = None

        if res:
            embedding = Card(res["id_card"], res["name"], res["embedded"]).get_embedded()
        return embedding

    def find_all():
        pass

    def id_search(id_card: int) -> Card:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')
                cursor.execute(
                    'SELECT * '
                    '  FROM "Card"       '
                    '  WHERE "idCard" = %(idCard)s',
                    {"idCard": id_card}
                )
                res = cursor.fetchall()

        return res

    def name_search(str) -> Card:
        pass

    def filter_cat_dao(self, filter: AbstractFilter):
        variable_filtered = filter.variable_filtered
        type_of_filtering = filter.type_of_filtering
        filtering_value = filter.filtering_value
        if type_of_filtering == "positive":
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                       "
                        "  FROM  Card                                   ",
                        "  WHERE variable_filtered LIKE filtering_value "
                    )
                    res = cursor.fetchall()
        if type_of_filtering == "negative":
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                       "
                        "  FROM  Card                                   ",
                        "  WHERE variable_filtered NOT LIKE filtering_value "
                    )
                    res = cursor.fetchall()
        return res

    def filter_num_dao(self, filter: AbstractFilter):
        variable_filtered = filter.variable_filtered
        type_of_filtering = filter.type_of_filtering
        filtering_value = filter.filtering_value
        if type_of_filtering == "higher_than":
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                       "
                        "  FROM  Card                                   ",
                        "  WHERE variable_filtered < filtering_value "
                    )
                    res = cursor.fetchall()
        if type_of_filtering == "lower_than":
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                       "
                        "  FROM Card                                    ",
                        "  WHERE variable_filtered > filtering_value "
                    )
                    res = cursor.fetchall()
        if type_of_filtering == "equal_to":
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                       "
                        "  FROM Card                                    ",
                        "  WHERE variable_filtered = filtering_value "
                    )
                    res = cursor.fetchall()
        return res

    def get_highest_id():
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')
                cursor.execute(
                    'SELECT MAX("idCard") '
                    '  FROM "Card"       '
                )
                res = cursor.fetchone()

        return res['max']


if __name__ == "__main__":
    print(CardDao.id_search(3))
