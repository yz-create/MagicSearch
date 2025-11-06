import os
import dotenv
import json
import csv

from unittest import mock

from utils.singleton import Singleton
from utils.embed import card_to_text
from db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """
    def start(self, data):
        """
        Reset the database, and import everything from the .json back

        Parameters:
        -----------
        data : dict
            The data directly extracted from the .json
        """
        mock.patch.dict(os.environ, {"POSTGRES_SCHEMA": "defaultdb"}).start()

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        print(os.getcwd())

        init_db = open("data/Untitled.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        init_db.close()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SET search_path TO defaultdb, public;')
                    cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
        except Exception:
            raise

        self.import_database(data)

    def import_database(self, data) -> None:
        """
        Import the entire database from .json into the SQL database

        Parameters:
        -----------
        data : dict
            The data directly extracted from the .json
        """
        color_list = []
        colors = []
        colorIdentities = []
        colorIndicators = []
        foreignDatas = []
        keyword_list = []
        keywords = []
        layouts = []
        sets = []
        printings = []
        subtype_list = []
        subtypes = []
        supertype_list = []
        supertypes = []
        type_list = []
        types = []
        legalities = []
        cards = []
        purchaseUrls = []
        rulings = []
        leadershipSkills_values = [{'brawl': True, 'commander': True, 'oathbreaker': True},
                                   {'brawl': False, 'commander': True, 'oathbreaker': True},
                                   {'brawl': True, 'commander': False, 'oathbreaker': True},
                                   {'brawl': True, 'commander': True, 'oathbreaker': False},
                                   {'brawl': False, 'commander': False, 'oathbreaker': True},
                                   {'brawl': False, 'commander': True, 'oathbreaker': False},
                                   {'brawl': True, 'commander': False, 'oathbreaker': False},
                                   {'brawl': False, 'commander': False, 'oathbreaker': False}]

        embed_cards = []

        with open("cards_with_embeddings.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                embed_cards.append(row)

        idCard = 0
        idRuling = 0
        column_with_na = ['asciiName', 'convertedManaCost', 'edhrecRank', 'edhrecSaltiness',
                          'faceManaValue', 'faceName', 'hasAlternativeDeckLimit', 'isFunny',
                          'isReserved', 'loyalty', 'manaCost', 'manaValue', 'power', 'side',
                          'text', 'toughness']
        url_list = ['tcgplayer', 'cardKingdom', 'cardmarket', 'cardKingdomFoil',
                    'cardKingdomEtched', 'tcgplayerEtched']
        foreignData_columns_with_na = ['faceName', 'flavorText', 'text', 'type']

        for i in data['data']:
            for card in data['data'][i]:
                card_dic = {}

                for color in card['colorIdentity']:
                    if color not in color_list:
                        color_list.append(color)
                    colorIdentities.append((idCard, color_list.index(color)))

                for color in card['colors']:
                    colors.append((idCard, color_list.index(color)))

                if 'colorIndicator' in card:
                    for color in card['colors']:
                        colorIndicators.append((idCard, color_list.index(color)))

                if 'defense' in card:
                    card_dic["defense"] = int(card["defense"])

                if 'foreignData' in card:
                    for foreignData in card['foreignData']:
                        foreignData_dic = {}
                        foreignData_dic['idCard'] = idCard
                        foreignData_dic['language'] = foreignData['language']
                        foreignData_dic['name'] = foreignData['name']
                        for column in foreignData_columns_with_na:
                            if column in foreignData:
                                foreignData_dic[column] = foreignData[column]
                        foreignDatas.append(foreignData_dic)

                if 'hand' in card:
                    card_dic["hand"] = int(card["hand"])

                if 'keywords' in card:
                    for keyword in card['keywords']:
                        if keyword not in keyword_list:
                            keyword_list.append(keyword)
                        keywords.append((idCard, keyword_list.index(keyword)))

                if card['layout'] not in layouts:
                    layouts.append(card['layout'])
                card_dic["layout"] = layouts.index(card["layout"])

                if 'leadershipSkills' in card:
                    card_dic["leadershipSkills"] = leadershipSkills_values.index(
                        card["leadershipSkills"]
                    )

                if 'legalities' in card:
                    legality_dic = {}
                    for legality in card['legalities']:
                        if card['legalities'][legality] == "Legal":
                            legality_dic[legality] = 0
                        elif card['legalities'][legality] == "Banned":
                            legality_dic[legality] = 1
                        else:
                            legality_dic[legality] = 2
                    if legality_dic not in legalities:
                        legalities.append(legality_dic)
                    card_dic["legalities"] = legalities.index(legality_dic)

                if 'life' in card:
                    card_dic["life"] = int(card["life"])

                card_dic["name"] = card["name"]

                if 'printings' in card:
                    for printing in card['printings']:
                        if printing not in sets:
                            sets.append(printing)
                        printings.append((idCard, sets.index(printing)))

                if 'firstPrinting' in card:
                    if card["firstPrinting"] not in sets:
                        sets.append(card["firstPrinting"])
                    card_dic["firstPrinting"] = sets.index(card["firstPrinting"])

                if 'purchaseUrls' in card:
                    purchaseUrls_dic = {}
                    purchaseUrls_dic['idCard'] = idCard
                    for url in url_list:
                        if url in card['purchaseUrls']:
                            purchaseUrls_dic[url] = card['purchaseUrls'][url]
                    purchaseUrls.append(purchaseUrls_dic)

                if 'rulings' in card:
                    for ruling in card['rulings']:
                        rulings.append((idRuling, idCard, ruling['date'], ruling['text']))
                        idRuling += 1

                for subtype in card['subtypes']:
                    if subtype not in subtype_list:
                        subtype_list.append(subtype)
                    subtypes.append((idCard, subtype_list.index(subtype)))

                for supertype in card['supertypes']:
                    if supertype not in supertype_list:
                        supertype_list.append(supertype)
                    supertypes.append((idCard, supertype_list.index(supertype)))

                if card['type'] not in type_list:
                    type_list.append(card['type'])
                card_dic["type"] = type_list.index(card["type"])

                for type_ in card['types']:  # type already means something in python, hence the _
                    if type_ not in type_list:
                        type_list.append(type_)
                    types.append((idCard, type_list.index(type_)))

                for column in column_with_na:
                    self.add_value_that_could_be_na(card, column, card_dic)

                card_dic["embed"] = embed_cards[idCard]["embed_detailed"]
                card_dic["shortEmbed"] = embed_cards[idCard]["embed_short"]

                cards.append(card_dic)
                idCard += 1

        color_values = [(i, color_list[i]) for i in range(len(color_list))]
        keyword_values = [(i, keyword_list[i]) for i in range(len(keyword_list))]
        layout_values = [(i, layouts[i]) for i in range(len(layouts))]
        set_values = [(i, sets[i]) for i in range(len(sets))]
        subtype_values = [(i, subtype_list[i]) for i in range(len(subtype_list))]
        supertype_values = [(i, supertype_list[i]) for i in range(len(supertype_list))]
        type_values = [(i, type_list[i]) for i in range(len(type_list))]

        legality_columns = ['commander', 'oathbreaker', 'duel', 'legacy', 'vintage', 'modern',
                            'penny', 'timeless', 'brawl', 'historic', 'gladiator', 'pioneer',
                            'predh', 'paupercommander', 'pauper', 'premodern', 'future',
                            'standardbrawl', 'standard', 'alchemy', 'oldschool']
        card_columns = ['layout', 'name', 'type', 'embed', 'shortEmbed', 'asciiName',
                        'convertedManaCost', 'defense', 'edhrecRank', 'edhrecSaltiness',
                        'faceManaValue', 'faceName', 'firstPrinting', 'hand',
                        'hasAlternativeDeckLimit', 'isFunny', 'isReserved', 'leadershipSkills',
                        'legalities', 'life', 'loyalty', 'manaCost', 'manaValue', 'power', 'side',
                        'text', 'toughness']
        purhcaseUrls_columns = ['idCard', 'tcgplayer', 'cardKingdom', 'cardmarket',
                                'cardKingdomFoil', 'cardKingdomEtched', 'tcgplayerEtched']
        foreignData_columns = ['idCard', 'language', 'name', 'faceName', 'flavorText', 'text',
                               'type']
        legality_values = self.fill_table_with_na_values(legality_columns, legalities)
        card_values = self.fill_table_with_na_values(card_columns, cards)
        purchaseUrls_values = self.fill_table_with_na_values(purhcaseUrls_columns, purchaseUrls)
        foreignData_values = self.fill_table_with_na_values(foreignData_columns, foreignDatas)

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.executemany(
                    'INSERT INTO "Color"("idColor", "colorName") VALUES (%s, %s)',
                    color_values
                )
                cursor.executemany(
                    'INSERT INTO "Keyword"("idKeyword", "name") VALUES (%s, %s)',
                    keyword_values
                )
                cursor.executemany(
                    'INSERT INTO "Layout"("idLayout", "name") VALUES (%s, %s)',
                    layout_values
                )
                cursor.executemany(
                    'INSERT INTO "Set"("idSet", "name") VALUES (%s, %s)',
                    set_values
                )
                cursor.executemany(
                    'INSERT INTO "Subtype"("idSubtype", "name") VALUES (%s, %s)',
                    subtype_values
                )
                cursor.executemany(
                    'INSERT INTO "Supertype"("idSupertype", "name") VALUES (%s, %s)',
                    supertype_values
                )
                cursor.executemany(
                    'INSERT INTO "Type"("idType", "name") VALUES (%s, %s)',
                    type_values
                )
                cursor.execute(
                    'INSERT INTO "LeadershipSkills"("idLeadership", "brawl", "commander", '
                    '"oathbreaker") VALUES'
                    '(0, True, True, True),'
                    '(1, True, True, False),'
                    '(2, True, False, True),'
                    '(3, False, True, True),'
                    '(4, False, False, True),'
                    '(5, False, True, False),'
                    '(6, True, False, False),'
                    '(7, False, False, False);'
                )
                cursor.execute(
                    'INSERT INTO "LegalityType"("idLegalityType", "type") VALUES'
                    '(0, %(Legal)s),'
                    '(1, %(Banned)s),'
                    '(2, %(Restricted)s);',
                    {
                        "Legal": "Legal",
                        "Banned": "Banned",
                        "Restricted": "Restricted",
                    },
                )
                cursor.executemany(
                    'INSERT INTO "Legality"("idLegality", "commander", "oathbreaker", "duel", '
                    '"legacy", "vintage", "modern", "penny", "timeless", "brawl", "historic", '
                    '"gladiator", "pioneer", "predh", "paupercommander", "pauper", "premodern", '
                    '"future", "standardbrawl", "standard", "alchemy", "oldschool") VALUES (%s, '
                    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                    '%s, %s)',
                    legality_values
                )
                cursor.executemany(
                    'INSERT INTO "Card"("idCard", "layout", "name", "type", "embed", "shortEmbed", '
                    '"asciiName", "convertedManaCost", "defense", "edhrecRank", '
                    '"edhrecSaltiness", "faceManaValue", "faceName", "firstPrinting", "hand", '
                    '"hasAlternativeDeckLimit", "isFunny", "isReserved", "leadershipSkills", '
                    '"legalities", "life", "loyalty", "manaCost", "manaValue", "power", "side", '
                    '"text", "toughness") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    card_values
                )
                cursor.executemany(
                    'INSERT INTO "Colors"("idCard", "idColor") VALUES (%s, %s)',
                    colors
                )
                cursor.executemany(
                    'INSERT INTO "ColorIndicator"("idCard", "idColor") VALUES (%s, %s)',
                    colorIndicators
                )
                cursor.executemany(
                    'INSERT INTO "ColorIdentity"("idCard", "idColor") VALUES (%s, %s)',
                    colorIdentities
                )
                cursor.executemany(
                    'INSERT INTO "Keywords"("idCard", "idKeyword") VALUES (%s, %s)',
                    keywords
                )
                cursor.executemany(
                    'INSERT INTO "Printings"("idCard", "idSet") VALUES (%s, %s)',
                    printings
                )
                cursor.executemany(
                    'INSERT INTO "Types"("idCard", "idType") VALUES (%s, %s)',
                    types
                )
                cursor.executemany(
                    'INSERT INTO "Supertypes"("idCard", "idSupertype") VALUES (%s, %s)',
                    supertypes
                )
                cursor.executemany(
                    'INSERT INTO "Subtypes"("idCard", "idSubtype") VALUES (%s, %s)',
                    subtypes
                )
                cursor.executemany(
                    'INSERT INTO "PurchaseURLs"("idPurchaseURLs", "idCard", "tcgplayer", '
                    '"cardKingdom", "cardmarket", "cardKingdomFoil", "cardKingdomEtched", '
                    '"tcgplayerEtched") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    purchaseUrls_values
                )
                cursor.executemany(
                    'INSERT INTO "ForeignData"("idForeign", "idCard", "language", "name", '
                    '"faceName", "flavorText", "text", "type") VALUES (%s, %s, %s, %s, %s, %s, %s, '
                    '%s)',
                    foreignData_values
                )
                cursor.executemany(
                    'INSERT INTO "Ruling"("idRuling", "idCard", "date", "text") VALUES (%s, %s, %s,'
                    ' %s)',
                    rulings
                )
            connection.commit()

    def fill_table_with_na_values(self, columns: list[str], values: list[dict]) -> list[tuple]:
        """
        Allows to fill the na values with None in a table, to make importing into SQL easier

        Parameters:
        -----------
        columns: list[str]
            The list containing all the columns' name
        values: list[dict]
            The list of all values of the table in a dictionnary form

        Returns:
        --------
        list[tuple]
            The list of all values, with None is the empty columns
        """
        values_as_tuple = []
        for i in range(len(values)):
            legality = [i]
            for j in columns:
                if j in values[i]:
                    legality.append(values[i][j])
                else:
                    legality.append(None)
            values_as_tuple.append(tuple(legality))

        return values_as_tuple

    def add_value_that_could_be_na(self, card: dict, column_name: str, card_dic: dict) -> None:
        """
        Allows to add in card_dic the value of the column in column_name if the card has it
        """
        if column_name in card:
            card_dic[column_name] = card[column_name]


if __name__ == "__main__":
    with open('AtomicCards.json', 'r') as file:
        data = json.load(file)
    ResetDatabase().start(data)
