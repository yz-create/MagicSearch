from pathlib import Path
import dotenv
import os

dotenv_path = Path(".env")
dotenv.load_dotenv(dotenv_path)
print("Host:", os.environ.get("POSTGRES_HOST"))
print("Port:", os.environ.get("POSTGRES_PORT"))
print("User:", os.environ.get("POSTGRES_USER"))
print("Database:", os.environ.get("POSTGRES_DATABASE"))