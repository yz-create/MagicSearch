"""import json
from collections import Counter

with open('AtomicCards.json', 'r') as file:
    data = json.load(file)

count = []
c = 0

for i in data['data']:
    for card in data['data'][i]:
        if "foreignData" in card:
            for url in card['foreignData']:
                c += 1"""
import csv

embed_cards = []

with open("cards_with_embeddings.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        embed_cards.append(row)

for card in embed_cards:
    if card["embed_detailed"] is None:
        print(card["idCard"])
