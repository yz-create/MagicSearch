import os
import dotenv
import json

from unittest import mock

from utils.singleton import Singleton
from utils.embedding_json_en_csv import card_to_text, embedding
from db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """
    def lancer(self, data):
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
        colors = []
        keywords = []
        layouts = []
        sets = []
        subtypes = []
        supertypes = []
        types = []
        legalities = []
        cards = []
        leadershipSkills_values = [{'brawl': True, 'commander': True, 'oathbreaker': True},
                                   {'brawl': False, 'commander': True, 'oathbreaker': True},
                                   {'brawl': True, 'commander': False, 'oathbreaker': True},
                                   {'brawl': True, 'commander': True, 'oathbreaker': False},
                                   {'brawl': False, 'commander': False, 'oathbreaker': True},
                                   {'brawl': False, 'commander': True, 'oathbreaker': False},
                                   {'brawl': True, 'commander': False, 'oathbreaker': False},
                                   {'brawl': False, 'commander': False, 'oathbreaker': False}]
        idCard = 0
        for i in data['data']:
            for card in data['data'][i]:
                card_dic = {'idCard': idCard}
                if 'asciiName' in card:
                    card_dic["asciiName"] = card['asciiName']
                card_dic["convertedManaCost"] = card['convertedManaCost']
                for color in card['colorIdentity']:
                    if color not in colors:
                        colors.append(color)
                if 'defense' in card:
                    card_dic["defense"] = int(card["defense"])
                if 'edhrecRank' in card:
                    card_dic["edhrecRank"] = card["edhrecRank"]
                if 'edhrecSaltiness' in card:
                    card_dic["edhrecSaltiness"] = card["edhrecSaltiness"]
                if 'faceManaValue' in card:
                    card_dic["faceManaValue"] = card["faceManaValue"]
                if 'faceName' in card:
                    card_dic["faceName"] = card["faceName"]
                if 'hand' in card:
                    card_dic["hand"] = int(card["hand"])
                if 'hasAlternativeDeckLimit' in card:
                    card_dic["hasAlternativeDeckLimit"] = card["hasAlternativeDeckLimit"]
                if 'isFunny' in card:
                    card_dic["isFunny"] = card["isFunny"]
                if 'isReserved' in card:
                    card_dic["isReserved"] = card["isReserved"]
                if 'keywords' in card:
                    for keyword in card['keywords']:
                        if keyword not in keywords:
                            keywords.append(keyword)
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
                    card_dic["legalities"] = legalities.index(card["legalities"])
                if 'life' in card:
                    card_dic["life"] = int(card["life"])
                if 'loyalty' in card:
                    card_dic["loyalty"] = card["loyalty"]
                if 'manaCost' in card:
                    card_dic["manaCost"] = card["manaCost"]
                card_dic["manaValue"] = card["manaValue"]
                card_dic["name"] = card["name"]
                if 'power' in card:
                    card_dic["power"] = card["power"]
                if 'printings' in card:
                    for printing in card['printings']:
                        if printing not in sets:
                            sets.append(printing)
                if 'firstPrinting' in card:
                    card_dic["firstPrinting"] = sets.index(card["firstPrinting"])
                if 'side' in card:
                    card_dic["side"] = card["side"]
                for subtype in card['subtypes']:
                    if subtype not in subtypes:
                        subtypes.append(subtype)
                for supertype in card['supertypes']:
                    if supertype not in supertypes:
                        supertypes.append(supertype)
                if 'text' in card:
                    card_dic["text"] = card["text"]
                if 'toughness' in card:
                    card_dic["toughness"] = card["toughness"]
                if card['type'] not in types:
                    types.append(card['type'])
                card_dic["type"] = card["type"]
                for type_ in card['types']:  # type already means something in python, hence the _
                    if type_ not in types:
                        types.append(type_)
                card_dic["text_to_embed"] = card_to_text(card)
                card_dic["embed"] = embedding(card_dic["text_to_embed"])
                cards.append(card_dic)
                idCard += 1

        color_values = [(i, colors[i]) for i in range(len(colors))]
        keyword_values = [(i, keywords[i]) for i in range(len(keywords))]
        layout_values = [(i, layouts[i]) for i in range(len(layouts))]
        set_values = [(i, sets[i]) for i in range(len(sets))]
        subtype_values = [(i, subtypes[i]) for i in range(len(subtypes))]
        supertype_values = [(i, supertypes[i]) for i in range(len(supertypes))]
        type_values = [(i, types[i]) for i in range(len(types))]

        legality_columns = ['commander', 'oathbreaker', 'duel', 'legacy', 'vintage', 'modern',
                            'penny', 'timeless', 'brawl', 'historic', 'gladiator', 'pioneer',
                            'predh', 'paupercommander', 'pauper', 'premodern', 'future',
                            'standardbrawl', 'standard', 'alchemy', 'oldschool']
        card_columns = ['idCard', 'convertedManaCost', 'layout', 'manaValue', 'name', 'type',
                        'text_to_embed', 'embed', 'asciiName', 'defense', 'edhrecRank',
                        'edhrecSaltiness', 'faceManaValue', 'faceName', 'firstPrinting', 'hand',
                        'hasAlternativeDeckLimit', 'isFunny', 'isReserved', 'leadershipSkills',
                        'legalities', 'life', 'loyalty', 'manaCost', 'power', 'side', 'text',
                        'toughness']
        legality_values = self.fill_table_with_na_values(legality_columns, legalities)
        card_values = self.fill_table_with_na_values(card_columns, cards)

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


if __name__ == "__main__":
    with open('AtomicCards.json', 'r') as file:
        data = json.load(file)
    ResetDatabase().lancer(data)


"""
Tables done:

Color
Keyword
Layout
Set
Subtype
Supertype
Type
LeadershipSkills
LegalityType
Legality

Tables not to fill:

User
Favourite
"""
