import logging
from psycopg2 import sql

from business_object.card import Card
from db_connection import DBConnection
from business_object.filters.abstract_filter import AbstractFilter


class CardDao:
    # Pattern Singleton : empêche la création de plusieurs objets,
    # renvoie toujours la même instance existante

    def create_card(card: Card) -> bool:
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

    def update_card(card: Card) -> bool:
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
                    cursor.execute('SET search_path TO defaultdb, public;')
                    cursor.execute(
                        'DELETE FROM "Card" WHERE "idCard" = %(idCard)s;',
                        {"idCard": card_id}
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error deleting card: {e}")
            return False

    # Probablement à supprimer
    def find_all_embedding(limit: int = 100, offset: int = 0) -> list[float]:
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

    def find_by_embedding(self, embed: list) -> list[float]:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')
                cursor.execute(
                    '''
                    SELECT "idCard"
                    FROM "Card"
                    WHERE "embed" = %(embed)s
                    ''',
                    {"embed": embed}
                )
                res = cursor.fetchone()
        if res:
            return CardDao().id_search(res["idCard"])
        else:
            return None

    def id_search(self, id_card: int) -> Card:
        """
        Returns all the information about the Card that has id_card as an id
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')
                cursor.execute(
                    'SELECT "idCard", "asciiName", "convertedManaCost", "defense", "edhrecRank", '
                    '"edhrecSaltiness", "embed", "faceManaValue", "faceName", "hand", '
                    '"hasAlternativeDeckLimit", "isFunny", "isReserved", "life", "loyalty", '
                    '"manaCost", "manaValue", c."name", "power", "side", "text", "toughness", '
                    'l."name" layout, t."name" type'
                    '  FROM "Card" c       '
                    '  JOIN "Layout" l ON l."idLayout" = c."layout"'
                    '  JOIN "Type" t ON t."idType" = c."type"'
                    '  WHERE "idCard" = %(idCard)s',
                    {"idCard": id_card}
                )
                res_card = cursor.fetchone()
                if res_card is None:
                    return None
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
                    SELECT s."name"
                    FROM "Set" s
                    JOIN "Card" c ON c."firstPrinting" = s."idSet"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_first_printing = cursor.fetchone()
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
                cursor.execute(
                    '''
                    SELECT *
                    FROM "LegalityType"
                    ORDER BY "idLegalityType" ASC
                    '''
                )
                res_legality_type = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "commander", "oathbreaker", "duel", "legacy", "vintage", "modern",
                    "penny", "timeless", "brawl", "historic", "gladiator", "pioneer", "predh",
                    "paupercommander", "pauper", "premodern", "future", "standardbrawl", "standard",
                    "alchemy", "oldschool"
                    FROM "Legality" l
                    JOIN "Card" c ON c."legalities" = l."idLegality"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_legalities = cursor.fetchone()
                cursor.execute(
                    '''
                    SELECT s."name"
                    FROM "Set" s
                    JOIN "Printings" p ON p."idSet" = s."idSet"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_printings = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "tcgplayer", "cardKingdom", "cardmarket", "cardKingdomFoil",
                    "cardKingdomEtched", "tcgplayerEtched"
                    FROM "PurchaseURLs"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_purchase_urls = cursor.fetchone()
                cursor.execute(
                    '''
                    SELECT "date", "text"
                    FROM "Ruling"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_rulings = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "name"
                    FROM "Subtype" s
                    JOIN "Subtypes" ss ON ss."idSubtype" = s."idSubtype"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_subtypes = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "name"
                    FROM "Supertype" s
                    JOIN "Supertypes" ss ON ss."idSupertype" = s."idSupertype"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_supertypes = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT "name"
                    FROM "Type" s
                    JOIN "Types" ss ON ss."idType" = s."idType"
                    WHERE "idCard" = %(idCard)s
                    ''',
                    {"idCard": id_card}
                )
                res_types = cursor.fetchall()

        color_identity = CardDao().get_list_from_fetchall(res_color_identity, 'colorName')
        color_indicator = CardDao().get_list_from_fetchall(res_color_indicator, 'colorName')
        colors = CardDao().get_list_from_fetchall(res_colors, 'colorName')
        if res_first_printing:
            first_printing = res_first_printing["name"]
        else:
            first_printing = None
        foreign_data = [dict(r) for r in res_foreign_data]
        keywords = CardDao().get_list_from_fetchall(res_keyword, 'name')
        if res_leadership_skills:
            leadership_skills = dict(res_leadership_skills)
        else:
            leadership_skills = None
        legality_types = {}
        for legality_type in res_legality_type:
            legality_types[legality_type["idLegalityType"]] = legality_type["type"]
        legalities = {}
        for legality in res_legalities:
            if res_legalities[legality] is not None:
                legalities[legality] = legality_types[res_legalities[legality]]
        printings = CardDao().get_list_from_fetchall(res_printings, "name")
        purchase_urls = {}
        if res_purchase_urls:
            for url in res_purchase_urls:
                if res_purchase_urls[url] is not None:
                    purchase_urls[url] = res_purchase_urls[url]
        rulings = []
        if res_rulings:
            for ruling in res_rulings:
                rulings.append({"date": ruling["date"], "text": ruling["text"]})
        subtypes = CardDao().get_list_from_fetchall(res_subtypes, "name")
        supertypes = CardDao().get_list_from_fetchall(res_supertypes, "name")
        types = CardDao().get_list_from_fetchall(res_types, "name")

        card = Card(
            res_card["idCard"], res_card["embed"], res_card["layout"], res_card["name"],
            res_card["type"], res_card["asciiName"], color_identity, color_indicator, colors,
            res_card["convertedManaCost"], res_card["defense"], res_card["edhrecRank"],
            res_card["edhrecSaltiness"], res_card["faceManaValue"], res_card["faceName"],
            first_printing, foreign_data, res_card["hand"], res_card["hasAlternativeDeckLimit"],
            res_card["isFunny"], res_card["isReserved"], keywords, leadership_skills, legalities,
            res_card["life"], res_card["loyalty"], res_card["manaCost"], res_card["manaValue"],
            res_card["power"], printings, purchase_urls, rulings, res_card["side"], subtypes,
            supertypes, res_card["text"], res_card["toughness"], types
            )

        return (card)

    def get_list_from_fetchall(self, res, column_name: str) -> list:
        """
        To transform a fetchall (which is a RealDictRow) of elements with one column into a list

        Parameters:
        -----------
        res: RealDictRow
            The result of the fetchall
        column_name: str
            The name of the column

        Return:
        -------
        list
            All elements of res as a list
        """
        returned_list = []
        for value in res:
            returned_list.append(value[column_name])
        return returned_list

    def name_search(self, name: str) -> list:
        """
        Returns all the information about the Cards that has name as their name

        Returns:
        --------
        list
            The list of all cards with said name (multiple cards can have the same name)
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')
                cursor.execute(
                    '''
                    SELECT "idCard"
                    FROM "Card"
                    WHERE "name" = %(name)s
                    ''',
                    {"name": name}
                )
                res = cursor.fetchall()

        cards = []
        for card in res:
            cards.append(CardDao().id_search(card["idCard"]))
        return cards

    def filter_dao(self, filter: AbstractFilter):
        """"
        This function checks that this is filter object and selects in the database the elements
        corresponding to the parameters of the filter
        First the function checks that type_of_filtering is in ["higher_than", "lower_than",
        "equal_to", "positive", "negative] as it is the easiest way to exclude non-filter objects
        Then we distinguish categorical and numerical filters and exclude objects with non-valid
        parameters
        Each time, we define a sql query and its parameters and comparator
        Finally, it selects the elements corresponding to the filter in the database

        Parameter :
        -----------
        filter : Abstracfilter
            filter we want to implement

        Return :
        --------
        list(Card)
        """
        try:
            variable_filtered = filter.variable_filtered
            type_of_filtering = filter.type_of_filtering
            filtering_value = filter.filtering_value

            if type_of_filtering not in ["higher_than", "lower_than", "equal_to", "positive", "negative"]:
                raise ValueError(
                    "This is not a filter : type_of_filtering can only take "
                    "'higher_than', 'lower_than', 'equal_to', 'positive' or 'negative' as input "
                    )
            sql_query = None
            sql_parameter = []

            if type_of_filtering in ["positive", "negative"]:  # categorical filter
                if variable_filtered not in ["type", "is_funny"]:
                    raise ValueError(
                        "variable_filtered must be in the following list : 'type', 'is_funny'"
                        )

                if not isinstance(filtering_value, str):
                    raise ValueError("filtering_value must be a string")

                sql_comparator = "LIKE" if type_of_filtering == "positive" else "NOT LIKE"
                sql_query = sql.SQL('SELECT * FROM "Card" WHERE {} {} %s').format(
                    sql.Identifier(variable_filtered),
                    sql.SQL(sql_comparator)
                )
                sql_parameter = [f"%{filtering_value}%"]

            else:  # numerical filter
                if variable_filtered not in ["mana_value", "defense", "edhrecRank", "toughness", "power"]:
                    raise ValueError("variable_filtered must be in the following list : mana_value, defense, edhrec_rank, toughness, power")
                if type_of_filtering == "higher_than": 
                    sql_comparator = ">"
                elif type_of_filtering == "equal_to":
                    sql_comparator = "="
                else:
                    sql_comparator = "<"
                sql_query = sql.SQL('SELECT * FROM "Card" WHERE {} {} %s').format(
                    sql.Identifier(variable_filtered),
                    sql.SQL(sql_comparator)
                )
                sql_parameter = [filtering_value]
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        logging.debug(f"Executing SQL: {sql_query.as_string(connection)} with params {sql_parameter}")
                        cursor.execute('SET search_path TO defaultdb, public;')
                        cursor.execute(sql_query, sql_parameter)
                        res = cursor.fetchall()
                        return res or []
        except Exception as e:
            logging.error(f"The input is not a filter : {e}")
            return False

    def get_highest_id(self) -> int:
        """
        Returns the highest id currently in the database
        """
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
    print(CardDao().get_similar_entries({'model': 'bge-m3:latest', 'embeddings': [[-0.010481069, 0.054576833, -0.040361676, -0.010884042, -0.023422036, 0.0044981306, 0.005991741, 0.04783862, -0.007369731, -0.019798117, -0.0078880945, 0.010494883, -0.020040197, -0.0021966312, 0.01552592, -0.026885586, -0.056760155, -0.005778143, -0.005819669, -0.039046925, -0.017710742, -0.0067253546, 0.081486255, 0.005323773, 0.016552888, 0.0040486944, -0.018844273, -0.0037244672, -0.0061085816, -0.00038674488, 0.03353667, -0.011790611, 0.020528046, -0.06800653, -0.051834904, -0.039035726, 0.0052831597, -0.029879678, -0.051570363, 0.020684492, 0.046003867, 0.0021183575, 0.0062039974, -0.007844098, 0.019558297, -0.0045237713, 0.03965065, -0.009187938, 0.0039889743, -0.01879753, 0.013796214, -0.0033138772, 0.057321355, -0.026868483, 0.013687231, 0.027030393, 0.02989174, -0.033674087, -0.06657985, -0.009346834, -0.008030193, 0.030639002, -0.009795985, 0.006203483, -0.0007012123, 0.01322421, 0.049995113, 0.010690325, -0.0066116606, -0.029935138, -0.0047267936, -0.008301097, 0.018378932, 0.01953529, -0.05819082, -0.017582044, 0.022977583, 0.019093614, 0.038672306, 0.0013138306, 0.09574743, 0.0181613, 0.034598846, 0.021631751, -0.0040559457, 0.0095516695, -0.0053138398, -0.053006094, 0.0014871848, -0.0066587995, -0.027615838, -0.045887478, 0.004638859, -0.012687088, -0.034232862, 0.032512672, -0.013973859, 0.035661083, 0.038580615, 0.00967979, 0.004221243, -0.0066284398, -0.014282438, -0.0475311, 0.050926287, -0.03094918, 0.005155487, 0.035170138, 0.03060748, 0.0064265956, 0.041762553, 0.019978002, 0.008878775, 0.048247036, 0.026685508, 0.012163308, 0.0006877584, 0.0004670993, 0.010331176, -0.02791602, 0.045278937, 0.0025296146, 0.06846562, 0.000945726, -0.029686917, -0.003721733, 0.03787215, 0.007970944, -0.045213755, -0.05674831, 0.037812468, 0.04855616, -0.028623214, -0.0034776914, 0.013251515, -0.002650881, -0.01012709, -0.02507838, -0.011039464, -0.031871237, 0.0013147197, 0.025693333, -0.01869137, -0.005139167, 0.026501438, -0.064835854, 0.016768014, -0.029643323, 0.029555995, -0.016122378, 0.04574661, -0.0033646459, 0.025507495, 0.0040877447, 0.013884957, 0.026940664, 0.0055692554, 0.022064203, 0.02008918, 0.029278858, 0.006398167, -0.03420968, 0.00017633343, 0.009534, -0.026995935, -0.006209915, 0.063644744, -0.018841686, -0.027285077, -0.005288038, 0.027674047, -0.041978538, 0.037071593, -0.045449242, 0.045383267, -0.010002969, 0.05237964, 0.034067005, 0.0073783905, -0.058463454, -0.015773883, 0.018242218, -0.029947313, -0.018818004, -0.0011589339, -0.026208071, 0.01100105, 0.013597787, 0.0026811853, -0.0006582094, -0.022284096, -0.040055975, 0.043396175, -0.048044693, 0.031128699, 0.024391597, 0.022865975, -0.0027233253, 0.019200051, -0.00020842288, -0.030255629, -0.0029478653, 0.013464184, -0.008230362, -0.02239363, 0.011244615, -0.058998372, -0.0053874357, 0.0317083, -0.07209952, -0.017430548, -0.015482034, -0.0032381953, 0.0052483277, 0.0031844892, 0.0046419594, -0.024456516, 0.003329252, 0.018334249, -0.049699504, -0.022023473, 0.03334474, 0.024302386, 0.012903784, 0.020809524, -0.010387998, 0.02858948, 0.040865567, 0.056358233, -0.063632645, 0.033397563, -0.020604499, -0.020476403, -0.031557422, -0.008551683, -0.009511951, -0.031664506, 0.03485721, 0.04172196, 0.020449104, 0.010612561, -0.010702748, 0.05940607, 0.0073669027, -0.06171151, -0.006866667, 0.02697001, -0.0018072766, -0.010909097, -0.029858809, -0.01722824, -0.012651583, -0.049577467, 0.023629563, 0.010558437, 0.010647621, 0.0003853044, -0.028976362, 0.016945926, -0.038008098, 0.0035485062, -0.009096663, 0.00043799778, 0.011057809, -0.020879278, 0.020387964, -0.014763445, 0.018276978, -0.015953615, -0.008480496, -0.026977386, -0.036693107, -0.012634261, -0.0115349535, -0.019618273, 0.070480414, 0.014203869, -0.046528585, 0.04352654, 0.017794395, -0.007878698, -0.010861102, -0.016364569, -0.010223244, -0.007698206, -0.03234239, 0.0057698027, -0.009940259, 0.032379568, -0.036558654, 0.034376767, -0.010627391, 0.07119235, -0.019865243, -0.008786926, 0.04063317, -0.014215013, -0.117061086, -0.023166811, -0.0376009, -0.02079922, 0.04317881, -0.014244218, -0.05192756, -0.01735939, -0.047002316, 0.013504112, -0.0059346934, -0.06321337, -0.023934003, 0.024265895, -0.009738878, 0.0055986806, -0.028279223, -0.046124667, -0.041255906, -0.046301387, -0.0048273, -0.03986709, 0.05255728, 0.00059936044, -0.031622484, -0.041787963, 0.05607832, -0.0634088, 0.0022659625, 0.010667865, 0.001117713, 0.02455785, -0.022236304, 0.027944794, 0.010063102, 0.03526164, -0.0056705223, -0.012603527, -0.008682603, 0.018817361, 0.02125145, 0.050278645, -0.014777941, 0.011843826, 0.024998212, 0.023383565, -0.0098648155, 0.032618307, -0.03372342, -0.014218797, 0.006269095, -0.010504267, 0.02929941, 0.018410372, -0.015005516, -0.016733661, 0.013292829, 0.05306487, -0.012204272, 0.011503466, -0.03756688, -0.07974378, 0.03270405, 0.034948114, -0.011937685, -0.0074463915, -0.03631762, -0.053102, -0.013915467, 0.0026572286, 0.034108788, -0.03925953, 0.008172855, -0.0066481046, 0.030783381, 0.0034178991, 0.030853625, 0.0013805589, 0.0007435717, -0.10755565, -0.0032138606, 0.017732928, -0.03060202, 0.0051284693, -0.0069498536, -0.049045324, -0.01387859, -0.001918921, 0.049018763, 0.32616168, 0.030214958, -0.0055059176, -0.034652103, -0.008205366, -0.016518494, -0.040678587, -0.005065887, 0.018035157, -0.040370066, 0.01948739, -0.01973231, -0.0043436834, 0.015263127, 0.0023178628, 0.024363257, 0.0052256617, -0.001566614, 0.11644798, 0.005164541, -0.0016119705, 0.008459083, 0.036323577, 0.0045447834, -0.03820867, -0.051680643, -0.03431301, 0.01925848, -0.02786762, -0.015727427, 0.003926605, 0.00721699, 0.035831988, -0.016226787, 0.002107918, 0.016730694, -0.00044523113, -0.026388003, 0.0012439566, 0.040921696, -0.015997719, -0.027650584, -0.025511596, 0.011665848, 0.018470228, -0.011405777, -0.029426318, -0.01554161, -0.011735978, 0.04619588, 0.007212069, 0.021844197, 0.0060814703, 0.018954402, 0.01935828, 0.017634885, -0.018187199, -0.02965434, 0.0059526595, 0.05444422, 0.019159505, 0.04534212, -0.025909763, 0.014872577, -0.008762187, 0.029965915, -0.009814357, 0.012625917, 0.016088618, 0.034413874, 0.04509675, 0.00090485165, 0.0025522355, 0.009748801, -0.011966756, 0.017154196, -0.014995538, 0.050182864, -0.0061334, 0.02637212, 0.0022757472, 0.0002615744, -0.032723617, -0.0044093127, -0.0071733096, 0.009073308, 0.033956867, 0.034588214, 0.009951465, -0.018698819, -0.016879166, -0.016387632, -0.021977358, -0.0032696617, -0.011143436, 0.03685388, 0.017911851, -0.023403592, -0.0031233134, -0.019582478, -0.028316712, -0.012612635, 0.012298777, -0.012670834, 0.013703613, -0.033976566, 0.038146086, 0.00084244076, 0.013356489, 0.027954688, 0.015390444, 0.02470818, -0.034822173, -0.05041074, -0.026524412, 0.0043372815, -0.032696385, 0.041260332, 0.023659158, 0.070502624, -0.013990474, 0.045881983, -0.0073449616, 0.00054438564, -0.010118133, -0.005029349, -0.0019834014, 0.040535696, -0.03390487, 0.050001197, 0.015903953, -0.035172664, 0.02232, 0.033739246, 0.007154491, 0.0030995775, 0.032034617, 0.047195725, 0.031621456, -0.00940545, 0.002757563, -0.034718394, -0.03112984, 0.032224957, -0.0010450039, 0.015948934, 0.010247418, 0.0054670903, -0.02383497, -0.01642074, 0.024231222, -0.039170135, 0.018055638, -0.0149897225, 0.008027698, -0.07479772, -0.0049844533, -0.040075604, -0.0326079, -0.03623668, -0.00499996, -0.026160862, 7.589003e-05, 0.061768644, 0.029451754, 0.018469602, 0.048299503, 0.012777294, 0.031526368, -0.023856958, 0.0022409013, 0.040125888, -0.043226965, 0.039815076, 0.018105367, -0.024549453, -0.040376917, -0.017786356, -0.048871707, -0.016383639, -0.0018556963, -0.075843275, 0.0088947695, 0.01759442, 0.0189917, 0.0029089877, 0.021275532, 0.003057379, 0.02446286, -0.016421024, -0.020739656, 0.051248755, -0.016197184, -0.011380288, 0.064280465, 0.037558217, 0.055661954, -0.02482351, 0.015617854, -0.02736849, 0.024315411, -0.012365627, -0.017541928, 0.008019397, -0.021751322, 0.016197737, -0.021215748, -0.011361884, -0.04879316, 0.030503118, -0.040061004, 0.0005890851, -0.02505402, -0.015779212, -0.066167206, 0.007876006, 0.060990315, 0.032238662, -0.029496, -0.01838089, -0.0034470095, -0.0027861584, 0.0033370506, -0.012348758, -0.01493559, -0.033836283, -0.016774043, -0.022316042, 0.03629734, 0.012738019, 0.003709583, -0.021448413, -0.02874309, -0.022558505, 0.035642833, -0.005322482, -0.0044438555, 0.03900743, -0.021171909, 0.015937448, 0.011664867, 0.03224133, 0.0312182, 0.07106138, -0.016005466, 0.021047167, -0.029757211, -0.042515226, -0.0011712974, -0.038395725, 0.0506305, -0.0013769475, 0.022519236, -0.035348546, -0.0012540289, 0.042915642, 0.035913475, -0.0226851, -0.046780128, 0.014256748, -0.018096516, 0.021211492, -0.008454293, 0.0071927216, 0.012957954, -0.050649073, -0.02515904, -0.007333792, -0.015752368, -0.043667406, -0.019286426, 0.019206872, 0.0031640283, -0.030771986, 0.010613293, 0.022968208, -0.0034797767, 0.016602028, 0.011995138, 0.03617834, -0.0069599347, 0.014677373, 0.0013697679, 0.05797807, -0.01906376, -0.016564997, 0.007971266, -0.0035761606, -0.014221388, 0.002620143, 0.002107307, 0.0198127, -0.047189042, 0.0119224815, -0.03601946, 0.020540934, -0.017857127, 0.016484866, -0.018399067, 0.031541843, -0.024523176, 0.038159326, -0.04573241, 0.010104583, -0.008900676, -0.009749542, -0.022788476, 0.0060632527, 0.040063746, -0.0010971483, 0.0266287, -0.07841845, 0.004273397, 0.023642682, -0.011215117, -0.0076106633, 0.022466587, -0.038767297, -0.01408946, 0.010528965, 0.03311698, -0.035062406, -0.012468332, 0.014748487, -0.029315526, -0.054537974, -0.010777597, 0.030250592, 0.00901215, -0.026839102, -9.551671e-05, -0.013062972, -0.030986879, -0.014328057, -0.002096822, 0.05742121, 0.033524893, 0.004447125, 0.006222548, 0.007563766, 0.026463082, 0.044734385, 0.050884735, -0.033046793, 0.0037399558, -0.007084848, 0.017894, 0.012099847, 0.045294344, 0.0010215666, 0.01806725, 0.017318562, -0.0031863407, -0.022610044, 0.046310637, -0.01595332, 0.023078835, 0.05446366, 0.03006361, -0.022380035, 0.017137975, 0.029701652, -0.04061339, -0.005874741, -0.039141465, -0.012032175, 0.026768418, 0.051613323, -0.035902385, -0.0024366167, 0.007183043, 0.050612964, -0.007950914, -0.043452464, -0.04339303, 0.022123571, -0.012356523, 0.015690597, 0.00679575, 0.004184182, 0.00406386, 0.0006507668, -0.007408766, -0.047025036, -0.010757634, -0.038312264, -0.04694137, 0.022200039, 0.0017988059, 0.01039974, -0.0131452335, 0.0052619735, 0.00024552454, 0.010302112, -0.2408324, -0.011958893, -0.0055644587, -0.0048846183, -0.012995935, 0.012000546, 0.010458787, 0.0058029387, -0.0307312, -0.058407944, -0.031730175, -0.026498003, 0.006030021, -0.003234065, -0.009864535, 0.0010180318, -0.032523654, 0.010028502, 0.0150792105, 0.06626929, -0.011959038, 0.0068795695, 0.010642495, 0.01721813, 0.014697675, -0.0071013314, 0.009646001, -0.018353278, -0.010666527, -0.04150631, 0.023631444, -0.06491493, 0.028062081, 0.054071978, 0.0012998694, 0.021961525, -0.003922681, 0.013542661, 0.008297695, -0.0032586297, 0.0141233895, -0.001963705, -0.038958784, -0.028064586, 0.0521213, 0.03392128, -0.01360198, -0.0052779648, -0.04850598, -0.03843275, -0.047431994, 0.017222162, 0.011407972, 0.014912765, -0.017646944, -0.034395345, -0.010288562, -0.019581389, -0.015830781, 0.023976047, -0.011258811, 0.013374013, -0.014140516, -0.05450057, -0.03243628, 0.011180141, -0.08734046, -0.0031084174, -0.016868548, 0.04428501, -0.015383454, 0.036580924, 0.02846374, -0.044257846, -0.02012567, 0.0042211916, 0.043072138, 0.002974385, -0.014919074, -0.022257617, -0.016621884, 0.022058126, 0.0024408717, 0.03922715, -0.027353993, 0.0053070225, -0.037960727, 0.0026270212, -0.048002474, -0.011650448, -0.01268706, -0.018950216, 0.016613351, 0.025281254, -0.009773222, -0.016559847, -0.010519436, -0.026030643, -0.021093085, -0.00949394, -0.031775843, 0.022186426, 0.052529383, -0.001009726, 0.015684845, 0.036726523, -0.0043808576, 0.015461432, 0.0018546652, 0.040307157, 0.0018550946, -0.017466458, -0.008060947, 0.01894196, -0.046642188, 0.010471028, -0.03848161, -0.011152222, -0.045714814, -0.006568459, -0.024065353, 0.018320609, 0.015817475, -0.012064913, -0.008459229, 0.008678994, 0.040917326, -0.010303616, -0.052128214, 0.006078369, 0.0064033736, -0.020889375, 0.017633406, 0.04653721, -0.0014275595, -0.0033492658, -0.03130261, 0.050959915, -0.03226945, -0.039745923, -0.034000125, 0.006662752, 0.007689708, -0.028376138, -0.026870437, 0.041870147, 0.050815877, -0.003134032, -0.05463219, -0.021462908, 0.05516608, -0.026871582, -0.0054842173, 0.053042136, -0.052921414, 0.018276634, -0.0030856621, -0.034760136, 0.014769468, -0.006451286, -0.01945448, 0.017310975, -0.04402148, -0.0046260897, -0.06090418, 0.023099894, 0.032037437, 0.00230366, -0.0774386, -0.013595222, -0.012643963, -0.009646459, -0.018305292, 0.046842393, 0.04527941, 0.021453407, 0.025501003, 0.037983924, 0.047217418, -0.044207253, 0.0026300813, 0.00085515383, 0.0029948077, 0.013594072, 0.006440043, -0.009039457, 0.022098009, -0.013560794, -0.015006782, 0.024622006, 0.021523476, 0.022374779, -0.0035062952, 0.0017310032, 0.051628437, -0.021559745, 0.006928295, -0.026971066, -0.012370897, -0.008204466, -0.049467742, -0.017319728, -0.022571113, -0.042690333, -0.008499487, -0.003641486, 0.009372441, 0.011314895, -0.022284986, 0.007224982, -0.0043025916, -0.034585558, -0.0155299, 0.037913084, -0.00038317463, 0.013351801, -0.010068236, 0.0044152965, -0.016251141, 0.011639326, 0.008104693, 0.012365835, 0.0035350174, -0.0056690937, -0.0087985275, 0.005740201, -0.031450428, 0.0151576465, 0.026642561, 0.031174412, -0.027619705, -0.0107533075, -0.028648665, 0.03602669, -0.009753338, -0.018398782, 0.050513435, -0.017872214, -0.06758157, -0.0013877073, -0.008564169, -0.016085904, -0.013654075, -0.013603994]], 'total_duration': 189620289, 'load_duration': 124291123, 'prompt_eval_count': 3}))
