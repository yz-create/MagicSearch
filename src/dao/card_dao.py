from business_object.card import Card
from dao.db_connection import DBConnection

class CardDao(metaclass=Singleton):
    # Pattern Singleton : empêche la création de plusieurs objets,
    # renvoie toujours la même instance existante

    def create_card(card : Card) -> bool:
        """
        Add a card to the database
        """


    def update_card(Card) -> bool:
        pass
    
    def delete_card(Card) -> bool:
        pass
    
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
                        #"  JOIN tp.pokemon_type pt USING(id_pokemon_type)                "
                        " WHERE c.name = %(name)s                                        ",
                        {"name": name},
                )
                res = cursor.fetchone()

            embedding = None

            if res:
                embedding = Card(res["id_card"], res["name"], res["embedded"]).get_embedded()
            return embedding
        
    
    def find_all() -> list(Card):
        pass
    
    def id_search(int) -> Card:
        pass

    def name_search(str) -> Card:
        pass
