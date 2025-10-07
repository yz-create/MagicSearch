import json
from collections import Counter

with open('AtomicCards.json', 'r') as file:
    data = json.load(file)

count = []

for i in data['data']:
    count.append(len(data['data'][i]))
    if len(data['data'][i]) == 5:
        for card in data['data'][i]:
            print(card)
            print("==============================")
    """card = data['data'][i][0]
    if card['colors'] != card['colorIdentity']:
        print("colors :", card['colors'])
        print("colorIdentity", card['colorIdentity'])"""

print(Counter(count))