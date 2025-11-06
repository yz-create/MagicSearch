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


def embedding(text: str) -> list:
    """
    Embeds a text into a vector (as a list)
    """
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
    print(type(json_response["embeddings"][0]))
    return json_response["embeddings"][0]


def card_to_text(card: dict) -> str:
    """
    Creates the text from a card that will be used to create the embed of said card.
    The card has to be a dict, meaning this function is only used for cards taken straight from the
    .json
    """
    colors = {"G": "Green", "R": "Red", "B": "Black", "W": "White", "U": "Blue"}
    card_colors = []
    for color in card["colorIdentity"]:
        card_colors.append(colors[color])
    fields = [
        card.get("name", ""),
        card.get("type", ""),
        card.get("type_line", ""),
        " ".join(card.get("supertypes", [])),
        " ".join(card.get("types", [])),
        " ".join(card.get("subtypes", [])),
        card.get("text", ""),
        f"Mana value: {card.get('manaValue', '')}",
        f"Colors: {', '.join(card_colors)}",
        f"Power: {card.get('power', '')}",
        f"Toughness: {card.get('toughness', '')}",
        f"Defense: {card.get('defense', '')}",
        f"Loyalty: {card.get('loyalty', '')}"
    ]
    return " | ".join([f for f in fields if f])


def add_embed_to_csv(card: dict, writer) -> None:
    """
    Adds the embedding of a card, as well as its id, to the .csv in the writer

    Parameters:
    -----------
    card: dict
        The card we wanna add the embedding of
    writer: '_csv.writer'
        The writer of .csv. Basically it allows to write into the csv
    """
    text_repr = card_to_text(card)
    emb = embedding(text_repr)  # liste de floats
    writer.writerow([
        idCard,
        json.dumps(emb)
    ])


if __name__ == "__main__":
    error = False

    with open("AtomicCards.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = []
    for set_name, card_list in data["data"].items():
        for card in card_list:
            cards.append(card)

    print(f"Nombre de cartes : {len(cards)}")

    with open("cards_with_embeddings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["id", "embedding"])

        idCard = 0
        for card in cards:
            print(card_to_text(card))
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
