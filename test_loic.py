import json
from collections import Counter

with open('AtomicCards.json', 'r') as file:
    data = json.load(file)

count = []
c = 0

for i in data['data']:
    for card in data['data'][i]:
        if 'legalities' in card:
            for j in card['legalities']:
                count.append(card['legalities'][j])
            c += 1
    """if c > 100:
        break"""

print(Counter(count))