import json
import requests
import os

# Charger le JSON
with open("AtomicCards.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cards = data["data"]  # accède au dictionnaire des cartes
first_card_name, first_card_list = next(iter(cards.items()))
first_card = first_card_list[0]

# print("Nom de la carte :", first_card_name)
# print("Infos :", first_card)

token = os.getenv("API_TOKEN")

url = "https://llm.lab.sspcloud.fr/ollama/api/embed"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-type": "application/json"}


def card_to_text_full(card: dict) -> str:
    """
    Transforme une carte en texte pour embedding,
    en gardant toutes les informations sauf 'printings' et 'purchaseUrls'.
    """
    # Faire une copie pour ne pas modifier l'objet original
    card_copy = card.copy()

    # Supprimer les champs à ignorer
    card_copy.pop("printings", None)
    card_copy.pop("purchaseUrls", None)

    # Convertir en JSON texte pour garder toutes les infos restantes
    # ensure_ascii=False pour garder les accents et caractères spéciaux
    text_repr = json.dumps(card_copy, ensure_ascii=False)

    return text_repr


# Exemple d'utilisation
card_info = {
    "name": '"Ach! Hans, Run!"',
    "colorIdentity": ["G", "R"],
    "colors": ["G", "R"],
    "convertedManaCost": 6.0,
    "firstPrinting": "UNH",
    "foreignData": [],
    "identifiers": {"scryfallOracleId": "a2c5ee76-6084-413c-bb70-45490d818374"},
    "isFunny": True,
    "layout": "normal",
    "legalities": {},
    "manaCost": "{2}{R}{R}{G}{G}",
    "manaValue": 6.0,
    "text": 'At the beginning of your upkeep, you may say "Ach! Hans, run! It\'s the . . ." and the name of a creature card. If you do, search your library for a card with that name, put it onto the battlefield, then shuffle. That creature gains haste. Exile it at the beginning of the next end step.',
    "type": "Enchantment",
    "types": ["Enchantment"],
    "subtypes": []
}

text_for_embedding = card_to_text_full(card_info)
# print(text_for_embedding)


def embedding(text: str):

    data = {
        "model": "bge-m3:latest",
        "input": text
    }

    response = requests.post(url, headers=headers, json=data)
    json_response = response.json()
    # res = json_response[ "embeddings"]
    return json_response


print(embedding(card_to_text_full(first_card))["embeddings"])
