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
                c += 1


print(Counter(count))

for i in None:
    print("a")

print("b")
