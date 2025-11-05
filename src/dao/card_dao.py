import logging

from business_object.card import Card
from db_connection import DBConnection
from business_object.filters.abstract_filter import AbstractFilter


class CardDao:
    # Pattern Singleton : empêche la création de plusieurs objets,
    # renvoie toujours la même instance existante

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

    def find_all(self):
        pass

    def id_search(self, id_card: int) -> Card:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')
                cursor.execute(
                    'SELECT "asciiName", "convertedManaCost", "defense", "edhrecRank", '
                    '"edhrecSaltiness", "embed", "faceManaValue", "faceName", "hand", '
                    '"hasAlternativeDeckLimit", "isFunny", "isReserved", "life", "loyalty", '
                    '"manaCost", "manaValue", c."name", "power", "side", "text", "toughness", '
                    'l."name" layout, t."name" type, s."name" firstPrinting'
                    '  FROM "Card" c       '
                    '  JOIN "Layout" l ON l."idLayout" = c."layout"'
                    '  JOIN "Type" t ON t."idType" = c."type"'
                    '  JOIN "Set" s ON s."idSet" = c."firstPrinting"'
                    '  WHERE "idCard" = %(idCard)s',
                    {"idCard": id_card}
                )
                res_card = cursor.fetchone()
                cursor.execute(
                    '''
                    SELECT "colorName"
                    FROM "Color" c
                    JOIN "ColorIdentity" ci ON ci."idColor" = c."idColor"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_color_identity = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "colorName"
                    FROM "Color" c
                    JOIN "ColorIndicator" ci ON ci."idColor" = c."idColor"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_color_indicator = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "colorName"
                    FROM "Color" c
                    JOIN "Colors" cs ON cs."idColor" = c."idColor"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_colors = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "language", "name", "faceName", "flavorText", "text", "type"
                    FROM "ForeignData"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_foreign_data = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "name"
                    FROM "Keyword" k
                    JOIN "Keywords" ks ON ks."idKeyword" = k."idKeyword"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_keyword = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "brawl", "commander", "oathbreaker"
                    FROM "LeadershipSkills" ls
                    JOIN "Card" c ON c."leadershipSkills" = ls."idLeadership"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_leadership_skills = cursor.fetchone()

        color_identity = CardDao.get_list_from_fetchall(res_color_identity, 'colorName')
        color_indicator = CardDao.get_list_from_fetchall(res_color_indicator, 'colorName')
        colors = CardDao.get_list_from_fetchall(res_colors, 'colorName')
        foreign_data = [dict(r) for r in res_foreign_data]
        keywords = CardDao.get_list_from_fetchall(res_keyword, 'name')
        if res_leadership_skills:
            leadership_skills = dict(res_leadership_skills)
        else:
            leadership_skills = None

        card = Card(
            res_card["embed"], res_card["layout"], res_card["name"], res_card["type"],
            res_card["asciiName"], color_identity, color_indicator, colors,
            res_card["convertedManaCost"], res_card["defense"], res_card["edhrecRank"],
            res_card["edhrecSaltiness"], res_card["faceManaValue"], res_card["faceName"],
            res_card["firstprinting"], foreign_data, res_card["hand"],
            res_card["hasAlternativeDeckLimit"], res_card["isFunny"], res_card["isReserved"],
            keywords, leadership_skills
            )

        return (
            res_card["embed"], res_card["layout"], res_card["name"], res_card["type"],
            res_card["asciiName"], color_identity, color_indicator, colors,
            res_card["convertedManaCost"], res_card["defense"], res_card["edhrecRank"],
            res_card["edhrecSaltiness"], res_card["faceManaValue"], res_card["faceName"],
            res_card["firstprinting"], foreign_data, res_card["hand"],
            res_card["hasAlternativeDeckLimit"], res_card["isFunny"], res_card["isReserved"],
            keywords, leadership_skills
            )

    def get_list_from_fetchall(res, column_name) -> list:
        returned_list = []
        for value in res:
            returned_list.append(value[column_name])
        return returned_list

    def name_search(self, str) -> Card:
        pass

    def filter_dao(filter: AbstractFilter):
        """"
        This function checks that this is filter object and selects in the database the elements corresponding
        to the parameters of the filter
        First the function checks that type_of_filtering is in ["higher_than", "lower_than", "equal_to", "positive", "negative]
        as it is the easiest way to exclude non-filter objects
        Then we distinguish categorical and numerical filters and exclude objects with non-valid parameters
        Finally, it selects the elements corresponding to the filter in the database
        
        Parameter :
        -----------
        filter : Abstracfilter
            filter we want to implement
        
        Return : 
        --------
        list(Card)
        """
        try :
            variable_filtered = filter.variable_filtered
            type_of_filtering = filter.type_of_filtering
            filtering_value = filter.filtering_value
            if type_of_filtering not in ["higher_than", "lower_than", "equal_to", "positive", "negative"]:
                    raise ValueError("This is not a filter : type_of_filtering can only take 'higher_than', 'lower_than', 'equal_to', 'positive' or 'negative' as input ")
            elif type_of_filtering in ["positive", "negative"]: # categorical filter
                if variable_filtered not in ["type", "is_funny"]:
                    raise ValueError("variable_filtered must be in the following list : 'type', 'is_funny'")
                if not isinstance(filtering_value, str):
                    raise ValueError("filtering_value must be a string")
                if type_of_filtering =="positive":
                    with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "SELECT *                                       "
                                "  FROM  Card                                   ",
                                "  WHERE variable_filtered LIKE filtering_value "
                            )
                            res = cursor.fetchall()
                else:
                    with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "SELECT *                                       "
                                "  FROM  Card                                   ",
                                "  WHERE variable_filtered NOT LIKE filtering_value "
                            )
                            res = cursor.fetchall()
                return res
            else : # numerical filter
                if variable_filtered not in ["manaValue", "defense", "edhrecRank", "toughness", "power"]:
                    raise ValueError("variable_filtered must be in the following list : manaValue, defense, edhrecRank, toughness, power")
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
                else : # equal_to
                    with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "SELECT *                                       "
                                "  FROM Card                                    ",
                                "  WHERE variable_filtered = filtering_value "
                            )
                            res = cursor.fetchall()
                return res

    def get_highest_id(self):
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
    print(CardDao.id_search(1))
