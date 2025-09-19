import json
import csv
import requests
import os

# ---- CONFIG ----
token = os.getenv("API_TOKEN")
# à mettre sur le terminal via https://llm.lab.sspcloud.fr/ << Réglages << Compte << copier la clé
# d'API
# si besoin mettre un export
# print("API_TOKEN:", token)
url = "https://llm.lab.sspcloud.fr/ollama/api/embed"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-type": "application/json"
}


# ---- Fonction pour appeler l'API d'embedding ----
def embedding(text: str):
    data = {
        "model": "bge-m3:latest",
        "input": text
    }
    response = requests.post(url, headers=headers, json=data)
    # response.raise_for_status()
    json_response = response.json()
    return json_response["embeddings"][0]  # vecteur (liste de floats)


# ---- Convertir une carte en texte pour l'embedding ----
def card_to_text(card: dict) -> str:
    fields = [
        card.get("name", ""),
        card.get("type", ""),
        " ".join(card.get("types", [])),
        " ".join(card.get("subtypes", [])),
        card.get("text", ""),
        card.get("manaCost", ""),
        f"Colors: {', '.join(card.get('colors', []))}",
    ]
    return " | ".join([f for f in fields if f])  # concaténation


# ---- Charger le JSON ----
with open("AtomicCards.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Format attendu : {"data": { "setName": [CardAtomic, ...], ...}}
cards = []
for set_name, card_list in data["data"].items():
    for card in card_list:
        cards.append(card)

print(f"Nombre de cartes : {len(cards)}")

# ---- Écriture du CSV ----
with open("cards_with_embeddings.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Header CSV
    writer.writerow([
        "name", "type", "manaCost", "colors", "text", "embedding"
    ])

    # Pour chaque carte
    for card in cards:
        try:
            text_repr = card_to_text(card)
            emb = embedding(text_repr)  # liste de floats
            writer.writerow([
                card.get("name", ""),
                card.get("type", ""),
                card.get("manaCost", ""),
                ",".join(card.get("colors", [])),
                card.get("text", ""),
                json.dumps(emb)  # stockage du vecteur en JSON dans une cellule CSV
            ])
        except Exception as e:
            print(f"Erreur avec la carte {card.get('name', '')}: {e}")
