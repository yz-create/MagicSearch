import logging
from psycopg2 import sql

from business_object.card import Card
from db_connection import DBConnection
from business_object.filters.abstract_filter import AbstractFilter
from utils.embed import embedding


class CardDao:

    def _get_or_create_id(
            self, cursor, table_name: str, id_column: str, name_column: str, value: str
            ) -> int:
        """
        Methods that either gets the id of the value in the table searched, or creates it if it
        doesn't exist

        Parameters
        ----------
        cursor : cursor
            The cursor for the database
        table_name : str
            Name of the table (ex: "Color", "Keyword")
        id_column : str
            Name of the id column (ex: "idColor", "idKeyword")
        name_column : str
            Name of the column that should contain the value (ex: "colorName", "name")
        value : str
            The value we want to know the id/create it

        Returns
        -------
        int
            The id of the value, either found or created
        """
        cursor.execute(
            f'SELECT "{id_column}" FROM "{table_name}" WHERE "{name_column}" = %(value)s',
            {"value": value}
        )
        result = cursor.fetchone()

        if result is None:
            cursor.execute(f'SELECT MAX("{id_column}") FROM "{table_name}"')
            id_max = cursor.fetchone()["max"]
            cursor.execute(
                f'INSERT INTO "{table_name}"("{id_column}", "{name_column}") VALUES ({id_max + 1},'
                f' %(value)s) RETURNING "{id_column}"',
                {"value": value}
            )
            result = cursor.fetchone()

        return result[id_column]

    def get_embed(self, card: Card):
        # Convertir la carte en texte puis calculer l'embedding
        # Construire le texte à partir de l'objet Card
        fields = [
            card.name or "",
            card.type_line or "",
            " ".join(card.supertypes) if card.supertypes else "",
            " ".join(card.types) if card.types else "",
            " ".join(card.subtypes) if card.subtypes else "",
            card.text or "",
            f"Mana cost: {card.mana_cost}" if card.mana_cost else "",
            f"Colors: {', '.join(card.colors)}" if card.colors else "",
            f"Power: {card.power}" if card.power else "",
            f"Toughness: {card.toughness}" if card.toughness else "",
            f"Defense: {card.defense}" if card.defense else "",
            f"Loyalty: {card.loyalty}" if card.loyalty else ""
        ]

        text_to_embed = " | ".join([f for f in fields if f])  # Filtrer les chaînes vides
        text_to_embed_short = card.name + ": " + card.text

        # Calculer l'embedding
        card_embedding = embedding(text_to_embed)
        card_short_embedding = embedding(text_to_embed_short)

        return (card_embedding, card_short_embedding)

    def get_or_create_all_ids_from_foreign_keys(self, card):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')

                # étapes 1, 2 et 3 avec _get_or_create_id

                # 1.1 Layout
                id_layout = self._get_or_create_id(
                    cursor, "Layout", "idLayout", "name", card.layout
                    )

                # 1.2 Type (le type principal)
                id_type = self._get_or_create_id(cursor, "Type", "idType", "name", card.type_line)

                # 1.3 FirstPrinting (Set)
                id_first_printing = None
                if card.first_printing:
                    id_first_printing = self._get_or_create_id(
                        cursor, "Set", "idSet", "name", card.first_printing
                        )

                # 1.4 LeadershipSkills
                id_leadership = None
                if card.leadership_skills:
                    cursor.execute(
                        '''
                        SELECT "idLeadership" FROM "LeadershipSkills"
                        WHERE "brawl" = %(brawl)s
                        AND "commander" = %(commander)s
                        AND "oathbreaker" = %(oathbreaker)s
                        ''',
                        {
                            "brawl": card.leadership_skills.get("brawl", False),
                            "commander": card.leadership_skills.get("commander", False),
                            "oathbreaker": card.leadership_skills.get("oathbreaker", False)
                        }
                    )
                    res_leadership = cursor.fetchone()
                    if res_leadership is None:
                        cursor.execute(
                            '''
                            INSERT INTO "LeadershipSkills"("brawl", "commander", "oathbreaker")
                            VALUES (%(brawl)s, %(commander)s, %(oathbreaker)s)
                            RETURNING "idLeadership"
                            ''',
                            {
                                "brawl": card.leadership_skills.get("brawl", False),
                                "commander": card.leadership_skills.get("commander", False),
                                "oathbreaker": card.leadership_skills.get("oathbreaker", False)
                            }
                        )
                        res_leadership = cursor.fetchone()
                    id_leadership = res_leadership["idLeadership"]

                # 1.5 Legalities
                id_legalities = None
                if card.legalities:
                    # Récupérer les LegalityType pour conversion
                    cursor.execute('SELECT * FROM "LegalityType" ORDER BY "idLegalityType" ASC')
                    res_legality_types = cursor.fetchall()
                    legality_type_map = {
                        lt["type"]: lt["idLegalityType"] for lt in res_legality_types
                        }

                    # Convertir les noms de légalité en IDs
                    legality_ids = {}
                    for format_name, legality_status in card.legalities.items():
                        if legality_status in legality_type_map:
                            legality_ids[format_name] = legality_type_map[legality_status]

                    # Construire la requête de recherche
                    if legality_ids:
                        where_clauses = ' AND '.join(
                            [f'"{k}" = %({k})s' for k in legality_ids.keys()]
                            )
                        query = f'SELECT "idLegality" FROM "Legality" WHERE {where_clauses}'
                        cursor.execute(query, legality_ids)
                        res_legality = cursor.fetchone()

                        if res_legality is None:
                            columns = ', '.join([f'"{k}"' for k in legality_ids.keys()])
                            placeholders = ', '.join([f'%({k})s' for k in legality_ids.keys()])
                            query = f'''
                                INSERT INTO "Legality"({columns})
                                VALUES ({placeholders})
                                RETURNING "idLegality"
                            '''
                            cursor.execute(query, legality_ids)
                            res_legality = cursor.fetchone()
                        id_legalities = res_legality["idLegality"]

                # 1.6 Colors (préparation des IDs)
                color_ids = {}
                if card.colors:
                    for color in card.colors:
                        color_ids[color] = self._get_or_create_id(
                            cursor, "Color", "idColor", "colorName", color
                            )

                # 1.7 ColorIdentity (préparation des IDs)
                color_identity_ids = {}
                if card.color_identity:
                    for color in card.color_identity:
                        if color not in color_ids:
                            color_identity_ids[color] = self._get_or_create_id(
                                cursor, "Color", "idColor", "colorName", color
                                )
                        else:
                            color_identity_ids[color] = color_ids[color]

                # 1.8 ColorIndicator (préparation des IDs)
                color_indicator_ids = {}
                if card.color_indicator:
                    for color in card.color_indicator:
                        if color not in color_ids and color not in color_identity_ids:
                            color_indicator_ids[color] = self._get_or_create_id(
                                cursor, "Color", "idColor", "colorName", color
                                )
                        elif color in color_ids:
                            color_indicator_ids[color] = color_ids[color]
                        else:
                            color_indicator_ids[color] = color_identity_ids[color]

                # 1.9 Keywords (préparation des IDs)
                keyword_ids = {}
                if card.keywords:
                    for keyword in card.keywords:
                        keyword_ids[keyword] = self._get_or_create_id(
                            cursor, "Keyword", "idKeyword", "name", keyword
                            )

                # 1.10 Types (préparation des IDs)
                type_ids = {}
                if card.types:
                    for type_name in card.types:
                        type_ids[type_name] = self._get_or_create_id(
                            cursor, "Type", "idType", "name", type_name
                            )

                # 1.11 Subtypes (préparation des IDs)
                subtype_ids = {}
                if card.subtypes:
                    for subtype in card.subtypes:
                        subtype_ids[subtype] = self._get_or_create_id(
                            cursor, "Subtype", "idSubtype", "name", subtype
                            )

                # 1.12 Supertypes (préparation des IDs)
                supertype_ids = {}
                if card.supertypes:
                    for supertype in card.supertypes:
                        supertype_ids[supertype] = self._get_or_create_id(
                            cursor, "Supertype", "idSupertype", "name", supertype
                            )

                # 1.13 Printings/Sets (préparation des IDs)
                printing_ids = {}
                if card.printings:
                    for printing in card.printings:
                        printing_ids[printing] = self._get_or_create_id(
                            cursor, "Set", "idSet", "name", printing
                            )
        return (
            id_layout, id_type, id_first_printing, id_leadership, id_legalities, color_ids,
            color_identity_ids, color_indicator_ids, keyword_ids, type_ids, subtype_ids,
            supertype_ids, printing_ids
            )

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

        # plusieurs étapes :
        # 1° lecture de toutes les nouvelles variables et de leur clés associées si elles existent
        # 2° vérification de l'existence de ces valeurs séparément dans chaque tables associées
        # 3° ajout de ces valeurs dans leur table associée si elles n'existaient pas
        # 4° ajout des informations de chaque valeurs de la nouvelle carte dans la table Card grace
        #    à leur clé étrangère
        # 5° rajouter l'id de la carte dans les tables : PurchaseURLs, Ruling, ForeignData

        # liste de nos tables :
        # tables des cartes : "Card", "Colors", "ColorIdentity", "ColorIndicator", -> "ForeignData",
        # "Keywords", "Legality", "Printings", -> "PurchaseURLs", -> "Ruling", "Subtypes",
        # "Supertypes", "Types"
        # table des users : "Favourite"

        # Pour l'étape 1 : on doit vérifier les tables Type, Layout, FirstPrinting,
        # LeadershipSkills, Legalities, Colors, ColorIdentity ColorIndicator, Keywords, Types,
        # Subtypes, Printings/Sets

        # Générer le nouvel ID de carte
        next_card_id = self.get_highest_id() + 1
        card_embedding, card_short_embedding = CardDao().get_embed(card)

        (
            id_layout, id_type, id_first_printing, id_leadership, id_legalities, color_ids,
            color_identity_ids, color_indicator_ids, keyword_ids, type_ids, subtype_ids,
            supertype_ids, printing_ids
        ) = CardDao().get_or_create_all_ids_from_foreign_keys(card)

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')

                # 4° création de la carte dans la table Card
                cursor.execute(
                    """
                    INSERT INTO "Card" (
                        "idCard", "layout", "name", "type", "embed", "shortEmbed"
                        "asciiName", "convertedManaCost", "defense", "edhrecRank",
                        "edhrecSaltiness", "faceManaValue", "faceName", "firstPrinting",
                        "hand", "hasAlternativeDeckLimit", "isFunny", "isReserved",
                        "leadershipSkills", "legalities", "life", "loyalty", "manaCost",
                        "manaValue", "power", "side", "text", "toughness"
                    ) VALUES (
                        %(idCard)s, %(layout)s, %(name)s, %(type)s, %(embed)s, %(shortEmbed)s,
                        %(asciiName)s, %(convertedManaCost)s, %(defense)s, %(edhrecRank)s,
                        %(edhrecSaltiness)s, %(faceManaValue)s, %(faceName)s,
                        %(firstPrinting)s, %(hand)s, %(hasAlternativeDeckLimit)s,
                        %(isFunny)s, %(isReserved)s, %(leadershipSkills)s,
                        %(legalities)s, %(life)s, %(loyalty)s, %(manaCost)s,
                        %(manaValue)s, %(power)s, %(side)s, %(text)s, %(toughness)s
                    ) RETURNING "idCard";
                    """,
                    {
                        "idCard": next_card_id,
                        "layout": id_layout,
                        "name": card.name,
                        "type": id_type,
                        "embed": card_embedding,
                        "shortEmbed": card_short_embedding,
                        "asciiName": card.ascii_name,
                        "convertedManaCost": card.converted_mana_cost,
                        "defense": card.defense,
                        "edhrecRank": card.edhrec_rank,
                        "edhrecSaltiness": card.edhrec_saltiness,
                        "faceManaValue": card.face_mana_value,
                        "faceName": card.face_name,
                        "firstPrinting": id_first_printing,
                        "hand": card.hand,
                        "hasAlternativeDeckLimit": card.has_alternative_deck_limit,
                        "isFunny": card.is_funny,
                        "isReserved": card.is_reserved,
                        "leadershipSkills": id_leadership,
                        "legalities": id_legalities,
                        "life": card.life,
                        "loyalty": card.loyalty,
                        "manaCost": card.mana_cost,
                        "manaValue": card.mana_value,
                        "power": card.power,
                        "side": card.side,
                        "text": card.text,
                        "toughness": card.toughness
                    }
                )
                result = cursor.fetchone()

                if result is None:
                    return False

                id_card = result["idCard"]

                # insertion dans les tables de jonction

                # Colors
                for color, id_color in color_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Colors"("idCard", "idColor")
                        VALUES (%(idCard)s, %(idColor)s)''',
                        {"idCard": id_card, "idColor": id_color}
                    )

                # ColorIdentity
                for color, id_color in color_identity_ids.items():
                    cursor.execute(
                        '''INSERT INTO "ColorIdentity"("idCard", "idColor")
                        VALUES (%(idCard)s, %(idColor)s)''',
                        {"idCard": id_card, "idColor": id_color}
                    )

                # ColorIndicator
                for color, id_color in color_indicator_ids.items():
                    cursor.execute(
                        '''INSERT INTO "ColorIndicator"("idCard", "idColor")
                        VALUES (%(idCard)s, %(idColor)s)''',
                        {"idCard": id_card, "idColor": id_color}
                    )

                # Keywords
                for keyword, id_keyword in keyword_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Keywords"("idCard", "idKeyword")
                        VALUES (%(idCard)s, %(idKeyword)s)''',
                        {"idCard": id_card, "idKeyword": id_keyword}
                    )

                # Types
                for type_name, id_t in type_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Types"("idCard", "idType")
                        VALUES (%(idCard)s, %(idType)s)''',
                        {"idCard": id_card, "idType": id_t}
                    )

                # Subtypes
                for subtype, id_subtype in subtype_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Subtypes"("idCard", "idSubtype")
                        VALUES (%(idCard)s, %(idSubtype)s)''',
                        {"idCard": id_card, "idSubtype": id_subtype}
                    )

                # Supertypes
                for supertype, id_supertype in supertype_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Supertypes"("idCard", "idSupertype")
                        VALUES (%(idCard)s, %(idSupertype)s)''',
                        {"idCard": id_card, "idSupertype": id_supertype}
                    )

                # Printings
                for printing, id_printing in printing_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Printings"("idCard", "idSet")
                        VALUES (%(idCard)s, %(idSet)s)''',
                        {"idCard": id_card, "idSet": id_printing}
                    )

                # PurchaseURLs
                if card.purchase_urls:
                    CardDao().insert_purchase_url(cursor, id_card, card)

                # ForeignData
                if card.foreign_data:
                    for foreign in card.foreign_data:
                        cursor.execute(
                            '''
                            SELECT MAX("idForeign")
                            FROM "ForeignData"
                            '''
                        )
                        id_max_foreign = cursor.fetchone()["max"]
                        cursor.execute(
                            """
                            INSERT INTO "ForeignData"(
                                "idForeign", "idCard", "language", "name", "faceName",
                                "flavorText", "text", "type"
                            ) VALUES (
                                %(idForeign)s, %(idCard)s, %(language)s, %(name)s, %(faceName)s,
                                %(flavorText)s, %(text)s, %(type)s
                            )
                            """,
                            {
                                "idForeign": id_max_foreign + 1,
                                "idCard": id_card,
                                "language": foreign.get("language"),
                                "name": foreign.get("name"),
                                "faceName": foreign.get("faceName"),
                                "flavorText": foreign.get("flavorText"),
                                "text": foreign.get("text"),
                                "type": foreign.get("type")
                            }
                        )

                # Rulings
                if card.rulings:
                    for ruling in card.rulings:
                        cursor.execute(
                            '''
                            SELECT MAX("idRuling")
                            FROM "Ruling"
                            '''
                        )
                        id_max_ruling = cursor.fetchone()["max"]
                        cursor.execute(
                            """
                            INSERT INTO "Ruling"("idRuling", "idCard", "date", "text")
                            VALUES (%(idRuling)s, %(idCard)s, %(date)s, %(text)s)
                            """,
                            {
                                "idRuling": id_max_ruling + 1,
                                "idCard": id_card,
                                "date": ruling.get("date"),
                                "text": ruling.get("text")
                            }
                        )

                connection.commit()
                return True

    def insert_purchase_url(self, cursor, id_card, card):
        cursor.execute(
            '''
            SELECT MAX("idPurchaseURLs")
            FROM "PurchaseURLs"
            '''
        )
        id_max_purchase_url = cursor.fetchone()["max"]
        cursor.execute(
            """
            INSERT INTO "PurchaseURLs"(
                "idPurchaseURLs", "idCard", "tcgplayer", "cardKingdom", "cardmarket",
                "cardKingdomFoil", "cardKingdomEtched", "tcgplayerEtched"
            ) VALUES (
                %(idPurchaseURLs)s, %(idCard)s, %(tcgplayer)s, %(cardKingdom)s,
                %(cardmarket)s, %(cardKingdomFoil)s, %(cardKingdomEtched)s,
                %(tcgplayerEtched)s
            )
            """,
            {
                "idPurchaseURLs": id_max_purchase_url + 1,
                "idCard": id_card,
                "tcgplayer": card.purchase_urls.get("tcgplayer"),
                "cardKingdom": card.purchase_urls.get("cardKingdom"),
                "cardmarket": card.purchase_urls.get("cardmarket"),
                "cardKingdomFoil": card.purchase_urls.get("cardKingdomFoil"),
                "cardKingdomEtched": card.purchase_urls.get("cardKingdomEtched"),
                "tcgplayerEtched": card.purchase_urls.get("tcgplayerEtched")
            }
        )

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
        card_embedding, card_short_embedding = CardDao().get_embed(card)

        (
            id_layout, id_type, id_first_printing, id_leadership, id_legalities, color_ids,
            color_identity_ids, color_indicator_ids, keyword_ids, type_ids, subtype_ids,
            supertype_ids, printing_ids
        ) = CardDao().get_or_create_all_ids_from_foreign_keys(card)

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO defaultdb, public;')

                # 4° création de la carte dans la table Card
                cursor.execute(
                    """
                    UPDATE "Card"
                    SET "layout"               = %(layout)s,
                        "name"                 = %(name)s,
                        "type"                 = %(type)s,
                        "embed"                = %(embed)s,
                        "shortEmbed"           = %(shortEmbed)s,
                        "asciiName"            = %(asciiName)s,
                        "convertedManaCost"    = %(convertedManaCost)s,
                        "defense"              = %(defense)s,
                        "edhrecRank"           = %(edhrecRank)s,
                        "edhrecSaltiness"      = %(edhrecSaltiness)s,
                        "faceManaValue"        = %(faceManaValue)s,
                        "faceName"             = %(faceName)s,
                        "firstPrinting"        = %(firstPrinting)s,
                        "hand"                 = %(hand)s,
                        "hasAlternativeDeckLimit" = %(hasAlternativeDeckLimit)s,
                        "isFunny"              = %(isFunny)s,
                        "isReserved"           = %(isReserved)s,
                        "leadershipSkills"     = %(leadershipSkills)s,
                        "legalities"           = %(legalities)s,
                        "life"                 = %(life)s,
                        "loyalty"              = %(loyalty)s,
                        "manaCost"             = %(manaCost)s,
                        "manaValue"            = %(manaValue)s,
                        "power"                = %(power)s,
                        "side"                 = %(side)s,
                        "text"                 = %(text)s,
                        "toughness"            = %(toughness)s
                    WHERE "idCard" = %(idCard)s;
                    """,
                    {
                        "idCard": card.id_card,
                        "layout": id_layout,
                        "name": card.name,
                        "type": id_type,
                        "embed": card_embedding,
                        "shortEmbed": card_short_embedding,
                        "asciiName": card.ascii_name,
                        "convertedManaCost": card.converted_mana_cost,
                        "defense": card.defense,
                        "edhrecRank": card.edhrec_rank,
                        "edhrecSaltiness": card.edhrec_saltiness,
                        "faceManaValue": card.face_mana_value,
                        "faceName": card.face_name,
                        "firstPrinting": id_first_printing,
                        "hand": card.hand,
                        "hasAlternativeDeckLimit": card.has_alternative_deck_limit,
                        "isFunny": card.is_funny,
                        "isReserved": card.is_reserved,
                        "leadershipSkills": id_leadership,
                        "legalities": id_legalities,
                        "life": card.life,
                        "loyalty": card.loyalty,
                        "manaCost": card.mana_cost,
                        "manaValue": card.mana_value,
                        "power": card.power,
                        "side": card.side,
                        "text": card.text,
                        "toughness": card.toughness
                    }
                )

                id_card = card.id_card

                # Colors
                CardDao().delete_from_table(cursor, "Colors", id_card)
                for color, id_color in color_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Colors"("idCard", "idColor")
                        VALUES (%(idCard)s, %(idColor)s)''',
                        {"idCard": id_card, "idColor": id_color}
                    )

                # ColorIdentity
                CardDao().delete_from_table(cursor, "ColorIdentity", id_card)
                for color, id_color in color_identity_ids.items():
                    cursor.execute(
                        '''INSERT INTO "ColorIdentity"("idCard", "idColor")
                        VALUES (%(idCard)s, %(idColor)s)''',
                        {"idCard": id_card, "idColor": id_color}
                    )

                # ColorIndicator
                CardDao().delete_from_table(cursor, "ColorIndicator", id_card)
                for color, id_color in color_indicator_ids.items():
                    cursor.execute(
                        '''INSERT INTO "ColorIndicator"("idCard", "idColor")
                        VALUES (%(idCard)s, %(idColor)s)''',
                        {"idCard": id_card, "idColor": id_color}
                    )

                # Keywords
                CardDao().delete_from_table(cursor, "Keywords", id_card)
                for keyword, id_keyword in keyword_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Keywords"("idCard", "idKeyword")
                        VALUES (%(idCard)s, %(idKeyword)s)''',
                        {"idCard": id_card, "idKeyword": id_keyword}
                    )

                # Types
                CardDao().delete_from_table(cursor, "Types", id_card)
                for type_name, id_t in type_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Types"("idCard", "idType")
                        VALUES (%(idCard)s, %(idType)s)''',
                        {"idCard": id_card, "idType": id_t}
                    )

                # Subtypes
                CardDao().delete_from_table(cursor, "Subtypes", id_card)
                for subtype, id_subtype in subtype_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Subtypes"("idCard", "idSubtype")
                        VALUES (%(idCard)s, %(idSubtype)s)''',
                        {"idCard": id_card, "idSubtype": id_subtype}
                    )

                # Supertypes
                CardDao().delete_from_table(cursor, "Supertypes", id_card)
                for supertype, id_supertype in supertype_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Supertypes"("idCard", "idSupertype")
                        VALUES (%(idCard)s, %(idSupertype)s)''',
                        {"idCard": id_card, "idSupertype": id_supertype}
                    )

                # Printings
                CardDao().delete_from_table(cursor, "Printings", id_card)
                for printing, id_printing in printing_ids.items():
                    cursor.execute(
                        '''INSERT INTO "Printings"("idCard", "idSet")
                        VALUES (%(idCard)s, %(idSet)s)''',
                        {"idCard": id_card, "idSet": id_printing}
                    )

                # PurchaseURLs
                if card.purchase_urls:
                    cursor.execute(
                        '''
                        SELECT *
                        FROM "PurchaseURLs"
                        WHERE ("idCard", "tcgplayer", "cardKingdom", "cardmarket",
                                "cardKingdomFoil", "cardKingdomEtched", "tcgplayerEtched")
                        IS NOT DISTINCT FROM
                        (%(idCard)s, %(tcgplayer)s, %(cardKingdom)s, %(cardmarket)s,
                        %(cardKingdomFoil)s, %(cardKingdomEtched)s, %(tcgplayerEtched)s)
                        ''',
                        {
                            "idCard": id_card,
                            "tcgplayer": card.purchase_urls.get("tcgplayer"),
                            "cardKingdom": card.purchase_urls.get("cardKingdom"),
                            "cardmarket": card.purchase_urls.get("cardmarket"),
                            "cardKingdomFoil": card.purchase_urls.get("cardKingdomFoil"),
                            "cardKingdomEtched": card.purchase_urls.get("cardKingdomEtched"),
                            "tcgplayerEtched": card.purchase_urls.get("tcgplayerEtched")
                        }
                    )
                    if cursor.fetchone() is None:
                        cursor.execute(
                            '''
                            SELECT MAX("idPurchaseURLs")
                            FROM "PurchaseURLs"
                            '''
                        )
                        id_max_purchase_url = cursor.fetchone()["max"]
                        cursor.execute(
                            """
                            INSERT INTO "PurchaseURLs"(
                                "idPurchaseURLs", "idCard", "tcgplayer", "cardKingdom", "cardmarket",
                                "cardKingdomFoil", "cardKingdomEtched", "tcgplayerEtched"
                            ) VALUES (
                                %(idPurchaseURLs)s, %(idCard)s, %(tcgplayer)s, %(cardKingdom)s,
                                %(cardmarket)s, %(cardKingdomFoil)s, %(cardKingdomEtched)s,
                                %(tcgplayerEtched)s
                            )
                            """,
                            {
                                "idPurchaseURLs": id_max_purchase_url + 1,
                                "idCard": id_card,
                                "tcgplayer": card.purchase_urls.get("tcgplayer"),
                                "cardKingdom": card.purchase_urls.get("cardKingdom"),
                                "cardmarket": card.purchase_urls.get("cardmarket"),
                                "cardKingdomFoil": card.purchase_urls.get("cardKingdomFoil"),
                                "cardKingdomEtched": card.purchase_urls.get("cardKingdomEtched"),
                                "tcgplayerEtched": card.purchase_urls.get("tcgplayerEtched")
                            }
                        )


                # ForeignData
                if card.foreign_data:
                    for foreign in card.foreign_data:
                        cursor.execute(
                            """
                            INSERT INTO "ForeignData"(
                                "idCard", "language", "name", "faceName",
                                "flavorText", "text", "type"
                            ) VALUES (
                                %(idCard)s, %(language)s, %(name)s, %(faceName)s,
                                %(flavorText)s, %(text)s, %(type)s
                            )
                            """,
                            {
                                "idCard": id_card,
                                "language": foreign.get("language"),
                                "name": foreign.get("name"),
                                "faceName": foreign.get("faceName"),
                                "flavorText": foreign.get("flavorText"),
                                "text": foreign.get("text"),
                                "type": foreign.get("type")
                            }
                        )

                # Rulings
                if card.rulings:
                    for ruling in card.rulings:
                        cursor.execute(
                            """
                            INSERT INTO "Ruling"("idCard", "date", "text")
                            VALUES (%(idCard)s, %(date)s, %(text)s)
                            """,
                            {
                                "idCard": id_card,
                                "date": ruling.get("date"),
                                "text": ruling.get("text")
                            }
                        )

                connection.commit()
                return True

    def delete_from_table(self, cursor, table, id_card):
        cursor.execute(
            '''DELETE FROM "%(table)s"
            WHERE "idCard" = %(idCard)s;
            ''',
            {"idCard": id_card,
             "table": table}
        )

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
                    '"manaCost", "manaValue", c."name", "power", "shortEmbed", "side", "text", '
                    '"toughness", l."name" layout, t."name" type'
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
        if res_legalities:
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
            res_card["idCard"], res_card["embed"], res_card["shortEmbed"], res_card["layout"],
            res_card["name"], res_card["type"], res_card["asciiName"], color_identity,
            color_indicator, colors, res_card["convertedManaCost"], res_card["defense"],
            res_card["edhrecRank"], res_card["edhrecSaltiness"], res_card["faceManaValue"],
            res_card["faceName"], first_printing, foreign_data, res_card["hand"],
            res_card["hasAlternativeDeckLimit"], res_card["isFunny"], res_card["isReserved"],
            keywords, leadership_skills, legalities, res_card["life"], res_card["loyalty"],
            res_card["manaCost"], res_card["manaValue"], res_card["power"], printings,
            purchase_urls, rulings, res_card["side"], subtypes, supertypes, res_card["text"],
            res_card["toughness"], types
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
        try :
            variable_filtered = filter.variable_filtered
            type_of_filtering = filter.type_of_filtering
            filtering_value = filter.filtering_value

            sql_query = None
            sql_parameter = []

            if type_of_filtering in ["positive", "negative"]:  # categorical filter
                
                if type_of_filtering == "positive":
                    sql_comparator = 'ILIKE'
                else:
                    sql_comparator = 'NOT ILIKE'
                    
                if variable_filtered == 'color':

                    sql_query = sql.SQL(
                        'SELECT* ' 
                        'FROM "Card" c '
                        'JOIN "Colors" a USING("idCard")'
                        'JOIN "Color" b USING ("idColor")'
                        'WHERE b."colorName" {} %s'
                        ).format(
                        sql.SQL(sql_comparator)
                    )
                    
                    sql_parameter = [f"%{filtering_value}%"]
                
                else:  # variable_filtered is type

                    sql_query = sql.SQL(
                        'SELECT * '
                        'FROM "Card" c '
                        'JOIN "Type" t ON c."type" = t."idType"'
                        'WHERE t."name" {} %s'
                        ).format(
                        sql.SQL(sql_comparator)
                    )
                    
                    sql_parameter = [f"%{filtering_value}%"]
            else:  # numerical filter
                
                if type_of_filtering == "higher_than": 
                    sql_comparator = ">"
                elif type_of_filtering == "equal_to":
                    sql_comparator = "="
                else:
                    sql_comparator = "<"
                if variable_filtered == "power":
                    sql_query = sql.SQL(
                        'SELECT * '
                        'FROM "Card" c '
                        'WHERE (CASE WHEN c."power" ~  %s THEN c."power"::int ELSE NULL END) {} %s').format(
                        sql.SQL(sql_comparator)
                    )
                    sql_parameter = ['^\d+$', filtering_value]
                elif variable_filtered == "toughness":
                    sql_query = sql.SQL(
                        'SELECT * '
                        'FROM "Card" c '
                        'WHERE (CASE WHEN c."toughness" ~  %s THEN c."toughness"::int ELSE NULL END) {} %s'
                    ).format(
                        sql.SQL(sql_comparator)
                    )
                    sql_parameter = ['^\d+$', filtering_value]
                else:
                    sql_query = sql.SQL(
                        'SELECT *'
                        'FROM "Card" WHERE {} {} %s'
                        ).format(
                        sql.Identifier(variable_filtered),
                        sql.SQL(sql_comparator)
                    )
                    sql_parameter = [filtering_value]
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    logging.debug(f"Executing SQL: {sql_query.as_string(connection)} with params {sql_parameter}")
                    print(cursor.mogrify(sql_query, sql_parameter))
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

    def get_similar_entries(self, conn, search_emb, use_short_embed=False):
        """
        Returns the 5 entries from the database with the embedding closest to the given
        [search_emb].
        
        Args:
            conn: Database connection
            search_emb: The embedding vector to search for
            use_short_embed: If True, uses 'shortEmbed' column, otherwise uses 'embed' column
        """
        conn.execute('SET search_path TO defaultdb, public;')
        
        embed_column = '"shortEmbed"' if use_short_embed else '"embed"'
        
        query = f"""
            SELECT
                "idCard",
                {embed_column} <-> %s as dst
            FROM "Card"
            ORDER BY dst
            LIMIT 5
        """
        
        results = conn.execute(query, (search_emb,))
        return results.fetchall()