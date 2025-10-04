import os
import dotenv

from unittest import mock

from utils.singleton import Singleton
from dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """
    def lancer(self):
        """Lancement de la réinitialisation des données
        Si test_dao = True : réinitialisation des données de test"""
        mock.patch.dict(os.environ, {"POSTGRES_SCHEMA": "defaultdb"}).start()

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        print(os.getcwd())

        init_db = open("src/data/Untitled.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        init_db.close()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
        except Exception:
            raise


if __name__ == "__main__":
    ResetDatabase().lancer()
