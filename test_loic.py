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
    try:
        # fore.append(card["side"])
        """for j in card["supertypes"]:
            fore.append(j)"""
        print(card["types"])
        c += 1
        if c > 9:
            break
    except:
        b += 1

print(Counter(fore))
print(c)
