from src.dao.user_dao import UserDao
from src.business_object.user import User
from src.db_connection import DBConnection

db = DBConnection()
cursor = db.connection.cursor()
cursor.execute("SELECT 1")
print(cursor.fetchone())


def test_create_user():
    print("=== TEST CREATE USER ===")

    # 1️⃣ Instancier le DAO avec la vraie connexion
    db = DBConnection()
    user_dao = UserDao(db)

    # 2️⃣ Créer un nouvel objet User (sans id)
    user = User(username="ilo", password="azerty123")
    print(f"Avant insertion → user_id = {user.user_id}")  # None

    # 3️⃣ Appeler la méthode DAO
    result = user_dao.create(user)

    # 4️⃣ Vérifier le résultat
    print(f"Résultat DAO : {result}")
    print(f"Après insertion → user_id = {user.user_id}")  # devrait contenir l'ID généré
    print("==========================")

if __name__ == "__main__":
    test_create_user()
