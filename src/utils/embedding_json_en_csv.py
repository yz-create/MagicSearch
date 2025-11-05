import json
import csv
import requests
import os
import time

# ---- CONFIG ----
token = os.getenv("API_TOKEN")
# (dans le terminal tu copies : export API_TOKEN= )
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
    global error
    data = {
        "model": "bge-m3:latest",
        "input": text
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print("❌ API Error:", response.status_code)
        print("Response text:", response.text)
        error = True

    try:
        json_response = response.json()
    except Exception:
        print("❌ Could not decode JSON response")
        print("Response text:", response.text)
        error = False
    return json_response["embeddings"][0]  # vecteur (liste de floats)


# ---- Convertir une carte en texte pour l'embedding ----
def card_to_text(card: dict) -> str:
    fields = [
        card.get("name", ""),
        card.get("type", ""),
        card.get("type_line", ""),
        " ".join(card.get("supertypes", [])),
        " ".join(card.get("types", [])),
        " ".join(card.get("subtypes", [])),
        card.get("text", ""),
        f"Mana cost: {card.get('manaCost', '')}",
        f"Colors: {', '.join(card.get('colors', []))}",
        f"Rarity: {card.get('rarity', '')}",
        f"Power: {card.get('power', '')}",
        f"Toughness: {card.get('toughness', '')}",
        f"Defense: {card.get('defense', '')}",
        f"Loyalty: {card.get('loyalty', '')}"
    ]
    return " | ".join([f for f in fields if f])  # concaténation lisible


def add_embed_to_csv(card, writer):
    text_repr = card_to_text(card)
    emb = embedding(text_repr)  # liste de floats
    writer.writerow([
        idCard,
        json.dumps(emb)
    ])


if __name__ == "__main__":
    error = False

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

        # Header CSV enrichi
        writer.writerow(["id", "embedding"])
        print("c")

        # Pour chaque carte
        idCard = 0
        for card in cards:
            time.sleep(0.5)
            try:
                add_embed_to_csv(card, writer)
            except Exception:
                print("Error with the card", card["idCard"])
                error = True
            while error:
                time.sleep(0.5)
                print("Error with the card", card["idCard"])
                try:
                    add_embed_to_csv(card, writer)
                    error = False
                except Exception:
                    error = True
            idCard += 1
