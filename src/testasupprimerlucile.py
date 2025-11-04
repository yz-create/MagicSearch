import psycopg2, os
from dotenv import load_dotenv
load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ.get("POSTGRES_PORT", 5432),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"]
    )
    print("✅ Connexion PostgreSQL réussie !")
except Exception as e:
    print("❌ Erreur :", e)