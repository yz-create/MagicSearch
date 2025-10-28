import json
from collections import Counter

with open('AtomicCards.json', 'r') as file:
    data = json.load(file)

type_lines = []

for i in data['data']:
    for card in data['data'][i]:
        if 'subtypes' in card:
            type_lines.append(card['subtypes'])

print(f"Nombre total de types uniques : {len(set(type_lines))}\n")
print("Liste complète des types :\n")

for t in sorted(set(type_lines)):
    print(t)





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
    """
    fields = [
        card.get("name", ""),
        card.get("type", ""),
        card.get("type_line", ""),
        " ".join(card.get("supertypes", [])),
        " ".join(card.get("types", [])),
        " ".join(card.get("subtypes", [])),
        card.get("text", ""),
        card.get("manaCost", ""),
        f"Colors: {', '.join(card.get('colors', []))}",
        f"Rarity: {card.get('rarity', '')}",
        f"Power: {card.get('power', '')}",
        f"Toughness: {card.get('toughness', '')}",
        f"Loyalty: {card.get('loyalty', '')}"
    ]
    """
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
    """
    writer.writerow([
        "name", "type", "type_line", "supertypes", "types", "subtypes",
        "manaCost", "colors", "rarity", "power", "toughness", "loyalty",
        "text", "embedding"
    ])
    """

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
        """
        try:
            text_repr = card_to_text(card)
            emb = embedding(text_repr)  # liste de floats
            writer.writerow([
                card.get("name", ""),
                card.get("type", ""),
                card.get("type_line", ""),
                " ".join(card.get("supertypes", [])),
                " ".join(card.get("types", [])),
                " ".join(card.get("subtypes", [])),
                card.get("manaCost", ""),
                ",".join(card.get("colors", [])),
                card.get("rarity", ""),
                card.get("power", ""),
                card.get("toughness", ""),
                card.get("loyalty", ""),
                card.get("text", ""),
                json.dumps(emb)
            ])
            """
        except Exception as e:
            print(f"Erreur avec la carte {card.get('name', '')}: {e}")
