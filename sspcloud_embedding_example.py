# Exemple d'utilisation de l'API 
# Ne rien pas modifier

import requests
import os

token = os.getenv("API_TOKEN")

url = "https://llm.lab.sspcloud.fr/ollama/api/embed"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-type": "application/json"}


def embedding(text: str):

    data = {
        "model": "bge-m3:latest",
        "input": text
    }

    response = requests.post(url, headers=headers, json=data)
    json_response = response.json()
    # res = json_response[ "embeddings"]
    return json_response


print(embedding("The sky is blue")["embeddings"])
