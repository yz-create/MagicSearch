# Exemple d'utilisation de l'API 
# Ne rien pas modifier

import requests
import os

token = os.getenv("API_TOKEN")
# (pour lucile : dans le terminal tu copies : export API_TOKEN= )
# à mettre sur le terminal via https://llm.lab.sspcloud.fr/ << Réglages << Compte << copier la clé
# d'API
# si besoin mettre un export
# print("API_TOKEN:", token)
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


print(embedding("The sky is blue"))
# print(embedding("The sky is blue")["embeddings"])
