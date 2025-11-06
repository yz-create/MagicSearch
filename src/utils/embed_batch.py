import json
import csv
import requests
import os
import time

token = os.getenv("API_TOKEN")

url = "https://llm.lab.sspcloud.fr/ollama/api/embed"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-type": "application/json"
}


BATCH_SIZE = 1_000  # Nombre de cartes à traiter en une seule requête


def embedding_batch(texts: list[str]) -> list[list]:
    """
    Envoie plusieurs textes à l'API en une seule requête
    """
    data = {
        "model": "bge-m3:latest",
        "input": texts
    }

    response = requests.post(url, headers=headers, json=data, timeout=300)

    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        return None

    json_response = response.json()
    return json_response["embeddings"]


def card_to_text_short(card: dict) -> str:
    """
    Convertit une carte en texte court : [name] : [description]
    """
    name = card.get("name", "Unknown")
    description = card.get("text", "No description")

    return f"{name}: {description}"


def card_to_text_detailed(card: dict) -> str:
    """
    Convertit une carte en texte détaillé avec toutes les informations
    """

    colors = {"G": "Green", "R": "Red", "B": "Black", "W": "White", "U": "Blue"}
    card_colors = []
    for color in card["colorIdentity"]:
        card_colors.append(colors[color])

    name = card.get("name", "Unknown")
    cost = card.get("manaCost", "no mana cost")
    card_type = card.get("type", "unknown type")
    description = card.get("text", "No description")

    # Construire la partie capacités
    capacities = []

    if card.get("type_line"):
        capacities.append(f"Type: {card.get('type_line')}")

    if card.get("supertypes"):
        capacities.append(f"Supertypes: {', '.join(card.get('supertypes'))}")

    if card.get("types"):
        capacities.append(f"Types: {', '.join(card.get('types'))}")

    if card.get("subtypes"):
        capacities.append(f"Subtypes: {', '.join(card.get('subtypes'))}")

    if card.get("colors"):
        capacities.append(f"Colors: {', '.join(card_colors)}")

    if card.get("power") and card.get("toughness"):
        capacities.append(f"Power/Toughness: {card.get('power')}/{card.get('toughness')}")

    if card.get("defense"):
        capacities.append(f"Defense: {card.get('defense')}")

    if card.get("loyalty"):
        capacities.append(f"Loyalty: {card.get('loyalty')}")

    text = (
        f"This is a MTG card with the name {name}. It costs {cost} to play. It is a {card_type}."
        f" It is described as follows: {description}."
    )

    if capacities:
        text += f" It has the following capacities: {'; '.join(capacities)}."

    return text


if __name__ == "__main__":
    with open("AtomicCards.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = []
    for set_name, card_list in data["data"].items():
        for card in card_list:
            cards.append(card)

    print(f"{len(cards)} cartes chargées")
    print("FO1a : Génération de deux embeddings par carte (short + detailed)")

    with open("cards_with_embeddings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "embed_short", "embed_detailed"])

        idCard = 0
        total_batches = (len(cards) + BATCH_SIZE - 1) // BATCH_SIZE

        for batch_num in range(total_batches):
            start_idx = batch_num * BATCH_SIZE
            end_idx = min(start_idx + BATCH_SIZE, len(cards))
            batch_cards = cards[start_idx:end_idx]

            # Convertir toutes les cartes du batch en textes (short and detailed)
            batch_texts = []
            for card in batch_cards:
                batch_texts.append(card_to_text_short(card))      # Texte court
                batch_texts.append(card_to_text_detailed(card))   # Texte détaillé

            try:
                batch_embeddings = embedding_batch(batch_texts)

                if batch_embeddings:
                    # Écrire les embeddings par paires (short, detailed)
                    for i in range(len(batch_cards)):
                        embed_short = batch_embeddings[i * 2]      # Indices pairs
                        embed_detailed = batch_embeddings[i * 2 + 1]  # Indices impairs
                        writer.writerow([
                            idCard,
                            json.dumps(embed_short),
                            json.dumps(embed_detailed)
                        ])
                        idCard += 1
                else:
                    # Si le batch échoue, traiter carte par carte (fallback)
                    print(f"Batch {batch_num+1}/{total_batches} échoué, traitement individuel...")
                    for card in batch_cards:
                        text_short = card_to_text_short(card)
                        text_detailed = card_to_text_detailed(card)
                        emb = embedding_batch([text_short, text_detailed])
                        if emb and len(emb) == 2:
                            writer.writerow([idCard, json.dumps(emb[0]), json.dumps(emb[1])])
                        else:
                            writer.writerow(
                                [idCard, json.dumps([0] * 1024), json.dumps([0] * 1024)]
                            )
                        idCard += 1
                        time.sleep(0.5)

            except Exception as e:
                print(f"Erreur batch {batch_num+1}/{total_batches}: {e}")
                # Fallback individuel
                for card in batch_cards:
                    try:
                        text_short = card_to_text_short(card)
                        text_detailed = card_to_text_detailed(card)
                        emb = embedding_batch([text_short, text_detailed])
                        if emb and len(emb) == 2:
                            writer.writerow([idCard, json.dumps(emb[0]), json.dumps(emb[1])])
                        else:
                            writer.writerow(
                                [idCard, json.dumps([0] * 1024), json.dumps([0] * 1024)]
                            )
                    except Exception:
                        writer.writerow([idCard, json.dumps([0] * 1024), json.dumps([0] * 1024)])
                    idCard += 1
                    time.sleep(0.5)

            # Afficher la progression
            if (batch_num + 1) % 10 == 0 or batch_num == total_batches - 1:
                progress = (batch_num + 1) / total_batches * 100
                print(f"   {progress:.1f}% - {idCard}/{len(cards)} cartes traitées")

            time.sleep(0.5)  # Petit délai entre les batches

    print(f"\nTerminé ! {idCard} cartes avec 2 embeddings chacune dans cards_with_embeddings.csv")
