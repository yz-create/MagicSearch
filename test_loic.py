import json
from collections import Counter

with open('AtomicCards.json', 'r') as file:
    data = json.load(file)

count = []
c = 0

for i in data['data']:
    for card in data['data'][i]:
        if "foreignData" in card:
            for url in card['foreignData']:
                print(url)


print(Counter(count))
