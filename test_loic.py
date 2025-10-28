import json
# from collections import Counter

with open('AtomicCards.json', 'r') as file:
    data = json.load(file)

count = []
c = 0

cards = []
for set_name, card_list in data["data"].items():
    for card in card_list:
        print(card)
        c += 1
    if c >= 1:
        break

for i in data['data']:
    for card in data['data'][i]:
        print(card)
    if c > 0:
        break

print(c)
