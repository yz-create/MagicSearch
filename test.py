import json

file = open("AtomicCards.json")
data = json.loads(file.read())

data = data['data']


print(data['Zoologist'][0]['identifiers'])
