import json

file = open("AtomicCards.json")
data = json.loads(file.read())

data = data['data']


for i in data:
    card = data[i][0]
    try:
        print(card['colorIdentity'])
    except:
        print("", end="")
