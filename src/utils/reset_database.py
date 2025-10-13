import os
import dotenv
import json

from unittest import mock

from utils.singleton import Singleton
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
        self.import_no_foreign(data)

    def import_no_foreign(self, data) -> None:
        """
        To import all the table that do not have any foreign keys, and therefore can be imported
        right away

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
        for i in data['data']:
            for card in data['data'][i]:
                for color in card['colorIdentity']:
                    if color not in colors:
                        colors.append(color)
                if 'keywords' in card:
                    for keyword in card['keywords']:
                        if keyword not in keywords:
                            keywords.append(keyword)
                if card['layout'] not in layouts:
                    layouts.append(card['layout'])
                if 'printings' in card:
                    for printing in card['printings']:
                        if printing not in sets:
                            sets.append(printing)
                for subtype in card['subtypes']:
                    if subtype not in subtypes:
                        subtypes.append(subtype)
                for supertype in card['supertypes']:
                    if supertype not in supertypes:
                        supertypes.append(supertype)
                if card['type'] not in types:
                    types.append(card['type'])
                for type_ in card['types']:  # type already means something in python
                    if type_ not in types:
                        types.append(type_)

        color_values = [(i, colors[i]) for i in range(len(colors))]
        keyword_values = [(i, keywords[i]) for i in range(len(keywords))]
        layout_values = [(i, layouts[i]) for i in range(len(layouts))]
        set_values = [(i, sets[i]) for i in range(len(sets))]
        subtype_values = [(i, subtypes[i]) for i in range(len(subtypes))]
        supertype_values = [(i, supertypes[i]) for i in range(len(supertypes))]
        type_values = [(i, types[i]) for i in range(len(types))]

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
            connection.commit()


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

Tables not to fill:

User
Favourite
"""
