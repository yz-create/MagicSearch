import json

file = open("AtomicCards.json")
data = json.loads(file.read())

data = data['data']

b = 0
c = 0
for i in data:
    card = data[i][0]
    try:
        print(card["leadershipSkills"])
        c += 1
        if c > 9:
            break
    except:
        b += 1
