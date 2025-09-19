import json
from collections import Counter

file = open("AtomicCards.json")
data = json.loads(file.read())

data = data['data']

b = 0
c = 0
fore = []
for i in data:
    card = data[i][0]
    for j in list(card.keys()):
        fore.append(j)
    try:
        # fore.append(card["power"])
        print(card["relatedCards"])
        """for j in list(card["purchaseUrls"].keys()):
            fore.append(j)"""
        c += 1
    except:
        b += 1

print(Counter(fore))
print(c)